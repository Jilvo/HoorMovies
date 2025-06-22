from datetime import datetime


def format_date(date_str):
    """
    Formats a date object to a string in the format 'YYYY-MM-DD'.

    Args:
        date (datetime.date): The date to format.

    Returns:
        str: The formatted date string.
    """
    if date_str is None:
        return None
    return datetime.strptime(date_str, "%Y-%m-%d").date()
