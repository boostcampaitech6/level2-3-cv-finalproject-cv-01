from datetime import datetime
from dateutil.relativedelta import relativedelta
import exchange_calendars as ecals

def valid_check(date):
    # date : 문자열 형태 : %Y-%m-%d
    XKRX = ecals.get_calendar("XKRX")
    return XKRX.is_session(date)
