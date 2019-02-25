"""
Various utilities for dates.
"""

from collections import namedtuple
import datetime
from datetime import timedelta
from calendar import month_name, monthrange, day_name
import sqlite3
from typing import Dict, Optional

__all__ = ['week_ending', 'date_table', 'load_date_table', 'holiday_name']

class DatefnError(Exception):
    pass

class BadDay(DatefnError):
    pass

def week_ending(date: datetime.date, week_ends_on: Optional[str] = 'Sat') -> datetime.date:
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
        'Sunday' : 'Sun',
        'Monday' : 'Mon',
        'Tuesday' : 'Tue',
        'Wednesday' : 'Wed',
        'Thursday' : 'Thu',
        'Friday' : 'Fri',
        'Saturday' : 'Sat',
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


def holiday_name(date: datetime.date, special_holidays: dict = None):
    "Return the holiday name (if any) for the date provided"
    holidays = special_holidays or {}
    if date in holidays:
        return holidays[date]

    first_weekday_of_month = monthrange(date.year, date.month)[0]
    if date.weekday() >= first_weekday_of_month:
        delta = date.weekday() - first_weekday_of_month
    else:
        delta = 7 + date.weekday() - first_weekday_of_month
    first_sameday_of_month = datetime.date(date.year, date.month, 1) + timedelta(days=delta)
    nth_day_of_month = (date - first_sameday_of_month).days // 7 + 1
    day_of_week = day_name[date.weekday()]

    if date.month == 1 and date.day == 1:
        return "New Year's"
    if date.month == 1 and day_of_week == 'Monday' and nth_day_of_month == 3:
        return 'Martin Luther King'
    if date.month == 2 and day_of_week == 'Monday' and nth_day_of_month == 3:
        return "President's Day"
    if date.month == 5 and day_of_week == 'Monday' and (date + timedelta(days=7)).month != date.month:
        return 'Memorial Day'
    if date.month == 7 and date.day == 3:
        return '4th of July'
    if date.month == 9 and day_of_week == 'Monday' and nth_day_of_month == 1:
        return 'Labor Day'
    if date.month == 11 and day_of_week == 'Thursday' and nth_day_of_month == 4:
        return 'Thanksgiving'
    # BUG! Won't be right when month starts on Friday
    if date.month == 11 and day_of_week == 'Friday' and nth_day_of_month == 4:
        return 'Day After Thanksgiving'
    if date.month == 12 and date.day == 24:
        return 'Christmas Eve'
    if date.month == 12 and date.day == 25:
        return 'Christmas'
    if date.month == 12 and date.day == 31:
        return "New Year's Eve"
    return None

def num_business_days_in_month(date: datetime.date, special_holidays: dict = None) -> int:
    "Return the number of business days in the month of the given date"
    this_date = datetime.date(date.year, date.month, 1)
    end_date = datetime.date(date.year, date.month, monthrange(date.year, date.month)[1])
    num_bus_days = 0
    while this_date <= end_date:
        if holiday_name(this_date) is None and this_date.weekday() < 5:
            num_bus_days += 1
        this_date += timedelta(days=1)
    return num_bus_days


def date_table(start_date: datetime.date, end_date: datetime.date) -> list:
    """
    Create a dates table for use in data warehouse environment
    
    The table will have one day for each day between "start_date" and
    "end_date" (inclusive of both).

    Fields included in table:
        - date_id (incrementing integer)
        - date_int (eg, 20140131)
        - date (eg, 2014-01-31)
        - year (eg, 2014)
        - quarter_int (eg, 3)
        - quarter (eg, Q3)
        - month_int (eg, 4)
        - month (eg, April)
        - month_end (eg, 2018-04-30)
        - day_of_month (eg, 27)
        - week_ending (eg, 2018-07-28) - note, weeks end on a saturday
        - day_of_week_int (0 = sunday, 7 = saturday)
        - day_of_week (eg, Monday)
        - year_month (eg, 201407)
        - holiday (eg, New Year's)
        - is_weekday (Yes/No)
        - is_holiday (Yes/No)
        - is_workday (Yes/No)
        - num_weekdays (1 for weekday, 0 otherwise)
        - num_holidays (1 for holiday, 0 otherwise)
        - num_workdays (1 for workday, 0 otherwise - workday = Mon-Fri and not a holiday)
        - week_num (eg, 1 = 1st week of year)
        - week_num_of_year (eg, 1 / 53 or 1 / 52)
        - weeks_remaining_in_year (eg, 52 if on week one in week with 53 weeks)
        - business_day_of_month (eg, 20)
        - business_days_in_month (eg, 22)
    """
    assert end_date >= start_date, "end_date must be after start_date"
    DateRow = namedtuple('DateRow', [
        'date_id',
        'date_int',
        'date',
        'year',
        'quarter_int',
        'quarter',
        'month_int',
        'month',
        'month_end',
        'day_of_month',
        'week_ending',
        'day_of_week_int',
        'day_of_week',
        'year_month',
        'holiday',
        'is_weekday',
        'is_holiday',
        'is_workday',
        'num_weekdays',
        'num_holidays',
        'num_workdays',
        'week_num',
        'week_num_of_year',
        'weeks_remaining_in_year',
        'business_day_of_month',
        'business_days_in_month',
    ])
    date = datetime.date(start_date.year, start_date.month, 1)
    dates = [] # type: ignore
    bus_days_in_month = {} # type: Dict[str, int]
    bus_day_of_mo = 0
    while date <= end_date:
        qtr = (date.month - 1) // 3 + 1
        holiday = holiday_name(date)
        if date.day == 1:
            bus_day_of_mo = 0
            bus_days_in_month[date.strftime("%Y%m")] = num_business_days_in_month(date)
        if holiday is None and date.weekday() < 5:
            bus_day_of_mo += 1
        if date < start_date:
            date += timedelta(days=1)
            continue
        dates.append(DateRow(
            len(dates),
            int(date.strftime('%Y%m%d')),
            date,
            date.year,
            qtr,
            'Q%d' % qtr,
            date.month,
            month_name[date.month],
            datetime.date(date.year, date.month, monthrange(date.year, date.month)[1]),
            date.day,
            week_ending(date, week_ends_on='Saturday'),
            (date.weekday() + 1) % 7, # default function has Monday = 0, Sunday = 6
            date.strftime("%A"),
            int(date.strftime("%Y%m")),
            holiday,
            'Yes' if date.weekday() < 5 else 'No', # is weekday?
            'Yes' if holiday else 'No', # is holiday?
            'Yes' if date.weekday() < 5 and holiday is None else 'No', # is workday?
            1 if date.weekday() < 5 else 0,
            1 if holiday else 0, # num holidays
            1 if not holiday and date.weekday() < 5 else 0, # num workdays
            date.isocalendar()[1],
            None,
            None,
            bus_day_of_mo,
            bus_days_in_month[date.strftime("%Y%m")],
        ))
        date += timedelta(days=1)
    return dates
