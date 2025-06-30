from zoneinfo import ZoneInfo
from django.utils.timezone import is_naive, make_aware
from rest_framework.exceptions import ValidationError


def convert_to_timezone(dt, tz_str):
    """
    Converts a timezone-aware or naive datetime to a specified timezone
    using Python's zoneinfo and Django utilities.

    Args:
        dt (datetime): The datetime object to convert. Can be naive or aware.
        tz_str (str): A valid timezone string (e.g., 'Europe/London', 'Asia/Kolkata').

    Returns:
        datetime: The datetime converted to the specified timezone.

    Raises:
        ValidationError: If the timezone string is invalid.

    Notes:
        - If the input datetime is naive (no timezone info), it will be made aware 
          using Django's default timezone before conversion.
        - This function requires Python 3.9+ and Django 4.0+.
    """
    try:
        tz = ZoneInfo(tz_str)
    except Exception:
        raise ValidationError(f"Unknown timezone: {tz_str}")
    
    if is_naive(dt):
        dt = make_aware(dt)
    
    return dt.astimezone(tz)
