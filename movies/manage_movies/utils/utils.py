from datetime import datetime


def format_date(date_str: str) -> str:
    """
    Formats a date object to a string in the format 'YYYY-MM-DD'."""
    if date_str is None:
        return None
    return datetime.strptime(date_str, "%Y-%m-%d").date()
