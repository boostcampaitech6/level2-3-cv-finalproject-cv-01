from datetime import datetime
import exchange_calendars as ecals
from datetime import datetime, timedelta

def valid_check(date):
    # date : 문자열 형태 : %Y-%m-%d
    XKRX = ecals.get_calendar("XKRX")
    return XKRX.is_session(date)


def logical_date(date):
    dt_date = datetime.strptime(date, '%Y-%m-%d')
    dt_ex_date = dt_date + timedelta(days=1)
    return dt_ex_date.strftime('%Y-%m-%d')
