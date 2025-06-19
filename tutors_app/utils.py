import re

def parse_price(text):
    """
    Extracts a normalized hourly price from strings like:
    '500 UAH/hour', '300 UAH/45 min', etc.
    Returns an integer price per 60 minutes.
    """
    match = re.search(r"(\d+)\s*UAH\s*/\s*(\d+)?\s*(min|hour)", text.lower())
    if not match:
        return None  # or raise an exception or log
    
    amount = int(match.group(1)) # к-сть грн
    duration = match.group(2) # тривалість (к-сть хв/год)
    unit = match.group(3) # одиниця ("хв" / "год")

    if unit == "hour" or duration is None:
        return amount
    else:
        minutes = int(duration)
        return round((amount / minutes) * 60) # потрібне округлення до 10