
from time import sleep
from datetime import datetime
import imp


imp.load_source('db.py', GRANULARITY, str(LOOKBACK))


def now():
    return datetime.now()


"""
while true:

    now
    sleep(60)
"""
