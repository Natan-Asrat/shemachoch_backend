import datetime
from django.conf import settings

def get_cycle():
    daysPassed = (datetime.date.today() - settings.CYCLE_START_DATE).days
    CYCLE_COUNT_NOW = settings.LAST_CYCLE_COUNT + 1 + daysPassed // settings.CYCLE_DURATION
    return CYCLE_COUNT_NOW
