import urllib
import requests
import pandas as pd
import logging
from datetime import datetime
import joblib
from importlib.resources import files
from pathlib import Path
from threading import local


def get_ticker_file():
    url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
    data = urllib.request.urlopen(url).read().decode()
    df = pd.read_json(data)
    return df


def fetch_holidays():
    url = "https://upstox.com/stocks-market/nse-bse-share-market-holiday-calendar-2023-india/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/80.0.3987.132 Safari/537.36"
    }
    r = requests.get(url, headers=headers)

    holiday_df = pd.read_html(r.text)[0]
    holiday_df["Date"] = pd.to_datetime(holiday_df["Date"], format="%d %B %Y")
    holidays = holiday_df["Date"].values
    holidays = holidays.astype("datetime64[D]")
    return holidays


def get_symbols():
    try:
        freeze_qty_url = "https://archives.nseindia.com/content/fo/qtyfreeze.xls"
        response = requests.get(freeze_qty_url, timeout=10)  # Set the timeout value
        response.raise_for_status()  # Raise an exception if the response contains an HTTP error status
        df = pd.read_excel(response.content)
        df.columns = df.columns.str.strip()
        df["SYMBOL"] = df["SYMBOL"].str.strip()
        return df
    except Exception as e:
        logger.error(f"Error while fetching symbols: {e}")
        return pd.DataFrame()


def load_iv_models():
    resource_path = files("volstreet").joinpath("iv_models")

    # noinspection PyTypeChecker
    curve_model_path = Path(resource_path.joinpath("iv_curve_adjuster.joblib"))
    # noinspection PyTypeChecker
    vix_to_iv_model_path = Path(resource_path.joinpath("vix_to_iv.joblib"))
    # noinspection PyTypeChecker
    atm_iv_on_expiry_day_model_path = Path(
        resource_path.joinpath("atm_iv_on_expiry_day.joblib")
    )

    models = []
    for model_path in [
        curve_model_path,
        vix_to_iv_model_path,
        atm_iv_on_expiry_day_model_path,
    ]:
        with open(model_path, "rb") as f:
            model = joblib.load(f)
            models.append(model)
    return tuple(models)


def create_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    today = datetime.now().strftime("%Y-%m-%d")

    # Create handlers

    # Info handler
    info_log_filename = f"info-{today}.log"
    info_handler = logging.FileHandler(info_log_filename)
    formatter = logging.Formatter(
        "%(asctime)s : %(levelname)s : %(name)s : %(message)s"
    )
    info_handler.setFormatter(formatter)
    info_handler.setLevel(logging.INFO)
    logger.addHandler(info_handler)

    # Error handler
    error_log_filename = f"error-{today}.log"
    error_handler = logging.FileHandler(error_log_filename)
    error_handler.setFormatter(formatter)
    error_handler.setLevel(logging.ERROR)
    logger.addHandler(error_handler)

    # Stream handler for console output
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.DEBUG)  # Set the level as per your requirement
    logger.addHandler(stream_handler)

    return logger


# Set the default values for critical variables
NOTIFIER_LEVEL = "INFO"
LARGE_ORDER_THRESHOLD = 10
ERROR_NOTIFICATION_SETTINGS = {"url": None}
LIMIT_PRICE_BUFFER = 0.01

# Create logger
logger = create_logger("volstreet")

# Get the list of scrips
scrips = get_ticker_file()
scrips["expiry_dt"] = pd.to_datetime(
    scrips[scrips.expiry != ""]["expiry"], format="%d%b%Y"
)
scrips["expiry_formatted"] = scrips["expiry_dt"].dt.strftime("%d%b%y")
scrips["expiry_formatted"] = scrips["expiry_formatted"].str.upper()

# Create a dictionary of token and symbol
token_symbol_dict = dict(zip(scrips["token"], scrips["symbol"]))

# Get the list of holidays
holidays = fetch_holidays()

# Get the list of symbols
symbol_df = get_symbols()

# Load the iv models
iv_curve_model, vix_to_iv_model, expiry_day_model = load_iv_models()

# Create a thread local object
thread_local = local()
