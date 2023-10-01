from datetime import datetime, timedelta

import pytz


def get_israel_time(subtract_days=0):
    today = datetime.today() - timedelta(subtract_days)
    israel_tz = pytz.timezone('Israel')
    israel_today = today.astimezone(israel_tz).strftime('%Y-%m-%d')
    return israel_today
