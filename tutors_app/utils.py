import re
import socket
from pathlib import Path
import requests
import logging
import time
from collections import Counter


def get_freq_dict(my_list):
    return Counter(my_list)


def is_connected():    # Для перевірки доступності інтернету перед відправленням запиту
    try:
        socket.create_connection(('www.google.com', 80), timeout=5)
        return True
    except OSError:
        return False


def get_file_path(fname):       # Визначаємо повний шлях до файлу fname
    return Path(__file__).parent / fname


# ---------- Decorators --------------------
def handle_exception(e, context=""):
    """
    Handles exceptions and returns a formatted error message.

    Args:
        e (Exception): The exception to handle.
        context (str): Additional context about where the error occurred.

    Returns:
        str: Formatted error message
    """
    error_messages = {
        requests.exceptions.Timeout: "Request timed out.",
        requests.exceptions.ConnectionError: "Could not connect to the server.",
        requests.exceptions.HTTPError: "HTTP error occurred.",
        AttributeError: "HTML structure issue.",
        ValueError: "Data issue.",
        requests.exceptions.RequestException: "Unexpected request error."
    }

    error_message = error_messages.get(type(e), f"Unexpected error: {e}")
    logging.error(f"{context} {error_message}")
    return error_message


def timer_elapsed(func):   # Для замірювання часу виконання ф-ції func
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f'Time elapsed in {func.__name__}: {end_time - start_time:.2f} seconds')
        return result
    return wrapper

# ------------- Parse logic --------------------------

def parse_price(text):
    """
    Extracts a normalized hourly price from strings like:
    '500 UAH/hour', '300 UAH/45 min',
    '500 грн/год', '300 грн/45 хв', etc.
    Returns an integer price per 60 minutes.
    """
    match = re.search(r"(\d+)\s*(грн|UAH)\s*/\s*(\d+)?\s*(хв|год|min|hour)", text.lower())
    if not match:
        return None  # or raise an exception or log
    
    amount = int(match.group(1)) # к-сть грн
    # unit_curr = match.group(2) # одиниця ("грн")
    duration = match.group(3) # тривалість (к-сть хв/год)
    unit_time = match.group(4) # одиниця ("хв" / "год")
    
    if unit_time == "год" or unit_time == "hour" or duration is None:
        return amount
    elif int(duration) == 45:
        # return round(amount * (4 / 3), -1) # округлення до 10
        return round(amount + (amount / 50) * 17, -1) # округлення до 10
        # amount * (4 / 3) == amount + amount * (1 / 3) == amount + (amount / 50) * (50 / 3), де (50 / 3) == (приблизно) 17
    else:
        minutes = int(duration)
        return round(amount * (60 / minutes), -1) # округлення до 10
    

# !!! Це зайва функція
# # def get_num_of_reviews(text):
# #     """
# #     Extracts a number of reviews from string like:
# #     '(відгуків: 31)'
# #     Returns an integer number of reviews.
# #     """
# #     return text[11:-1].strip()
# # # number_of_reviews