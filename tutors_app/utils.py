import re

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
    else:
        minutes = int(duration)
        # return round((amount / minutes) * 60, -1) # округлення до 10
        return round(amount * (60 / minutes), -1) # округлення до 10


def get_num_of_reviews(text):
    """
    Extracts a number of reviews from string like:
    '(відгуків: 31)'
    Returns an integer number of reviews.
    """
    return text[11:-1].strip()
# number_of_reviews