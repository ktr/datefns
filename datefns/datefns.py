"""
Various utilities for dates.
"""

from datetime import date, timedelta

class DatefnError(Exception):
    pass

class BadDay(DatefnError):
    pass

def week_ending(date, week_ends_on='Sat'):
    "Return the date of"
    days = {
        'Mon' : 'Mon',
        'M' : 'Mon',
        'Tue' : 'Tue',
        'Tu' : 'Tue',
        'Wed' : 'Wed',
        'W' : 'Wed',
        'Thu' : 'Thu',
        'Th' : 'Thu',
        'Fri' : 'Fri',
        'F' : 'Fri',
        'Sat' : 'Sat',
        'Sa' : 'Sat',
        'Sun' : 'Sun',
        'Su' : 'Sun',
    }
    if week_ends_on not in days:
        raise BadDay("Cannot understand '%s' for week_ends_on argument" % week_ends_on)
    offsets = {
        'Mon' : 6,
        'Tue' : 5,
        'Wed' : 4,
        'Thu' : 3,
        'Fri' : 2,
        'Sat' : 1,
        'Sun' : 0,
    }
    offset = offsets[days[week_ends_on]]
    start = date - timedelta(days=(date.weekday() + offset) % 7)
    end = start + timedelta(days=6)
    return end
