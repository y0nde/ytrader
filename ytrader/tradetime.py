import pandas as pd
import datetime as dt
import jpholiday as jh


class Tradetime:
    def __init__(self, time=None):
        self.set_time(time)
    
    def set_time(self, time=None):
        if time:
            self.time = time
        else:
            self.time = dt.datetime.now().date()
        if not is_business_day(self.time):
            self.time = self.previous_date(1)

    def set_next_date(self,date_n):
        for _ in range(date_n):
            self.time=next_business_date(self.time)

    def previous_date(self,date_n):
        return previous_n_date(self.time,date_n)

    def update(self):
        self.set_next_date(1)



def is_business_day(date) -> bool:
    '''
    Check if the specified date is a business day of TSE or not.

    Parameters
    ----------
    date : dt.date
        date which will be checked

    Returns
    -------
    date_is_business_day : bool
        True if it is, and vice versa
    '''
    if isinstance(date, dt.datetime):
        date=date.date()
    if date.weekday() == 5 or date.weekday() == 6:  # Saturday, Sunday
        return False
    if jh.is_holiday(date):
        return False
    if date.month == 1 and (date.day == 2 or date.day == 3):
        return False
    if date.month == 12 and date.day == 31:
        return False
    # 東証鯖落ち日
    if date == dt.date(2020,10,1):
        return False
    return True

def next_business_date(date) -> dt.datetime:
    '''
    Return dt.date of the next business day of the specified date.

    Parameters
    ----------
    date : dt.date
    include : bool
        when True and the specified date is a business day, return date immediately
    '''
    if isinstance(date, dt.datetime):
        date=date.date()
    while True:
        date += dt.timedelta(days=1)
        if is_business_day(date):
            return date

def previous_n_date(date,n) -> dt.date:
    '''
    Return dt.date of the previous business day of the specified date.

    Parameters
    ----------
    date : dt.date
    include : bool
        when True and the specified date is a business day, return date immediately
    '''
    count=0
    while count<n:
        date -= dt.timedelta(days=1)
        if is_business_day(date):
            count+=1
    return date
