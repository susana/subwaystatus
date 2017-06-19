import time
from pytz import UTC

import arrow


def get_upcoming_hour():
    return arrow.utcnow().replace(
        hours=+1,
        minute=0,
        second=0,
        microsecond=0).datetime.replace(tzinfo=UTC)


def get_local_time():
    local_tz_nondst, local_tz_dst = time.tzname
    local_tz = local_tz_dst or local_tz_nondst
    return arrow.utcnow().to(local_tz)
