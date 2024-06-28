import datetime


def unix_to_date(unix_time: int) -> datetime.date:
    utc_datetime = datetime.datetime.fromtimestamp(unix_time/1000, datetime.timezone.utc)

    return utc_datetime.date()
