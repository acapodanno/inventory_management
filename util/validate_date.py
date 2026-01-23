from datetime import datetime

def validate_date(date):
    """ Validate if the provided date string is in YYYY-MM-DD format. """
    if isinstance(date, str):
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    return False