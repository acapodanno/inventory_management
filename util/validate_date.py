from datetime import datetime

def validate_date(date):
    if isinstance(date, str):
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    return False