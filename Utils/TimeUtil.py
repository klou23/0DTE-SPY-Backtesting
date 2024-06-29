from datetime import datetime, timezone, date, time

import pytz


def unix_to_date(unix_time: int) -> date:
    utc_datetime = datetime.fromtimestamp(unix_time/1000, timezone.utc)

    return utc_datetime.date()


def unix_to_time(unix_time: int) -> time:
    utc_datetime = datetime.fromtimestamp(unix_time/1000, timezone.utc)

    ny_tz = pytz.timezone('America/New_York')
    ny_datetime = utc_datetime.astimezone(ny_tz)

    return ny_datetime.time()
