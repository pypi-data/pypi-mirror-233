""" Collection of functions to help you with dates... get it??? """

import pandas as pd
import re


def end_of_period(today: pd.Timestamp, freq: str) -> pd.Timestamp:
    """ Calculate End of Last Month / Last Week Given pd.Timestamp & Freq """

    match freq.lower():
        case 'w':
            # weekday 4 is a Friday
            # Week n+1 will find next Friday... even if today is Friday
            # hack -7 days will reverse 7 days from next Friday. BOOM.
            return today + pd.offsets.Week(n=1, weekday=4) - pd.DateOffset(7)
        case 'm':
            # on month end we +MonthEnd(n=1) to get the end of current month
            # then subtract one full month... otherwise weird things happen
            return today + pd.offsets.MonthEnd(1) - pd.offsets.MonthEnd(1)


def flex_date_solver(
        date_input: str | pd.Timestamp = "12M",
        eop: bool = False,
        today: str = "today") -> pd.Timestamp:
    """ Flexible Date Solver for finding Relative Dates

    Originally written for finnhub calls but made more general. Takes either a
    date string or a 'relative' date statement and spits out the pd.Timestamp.
    Useful to allow someone to specify fixed date string or relative as input.

    params:
    - date_input: str | pd.Timestamp (default == '12m') which can be:
        1. date string i.e. '2020-12-31' which can be read by pd.Datetime
        2. relative string i.e. '-5Y'; valid freq are D, W, M, Y
        3. timestamp is converted to date-string and continue as normal
    - eop: bool (default == False) and is flag for 'end of period'
    - today: str (default == "today") t1 relative date; reads into pd.Datetime

    returns:
    - pd.Timestamp """

    # Input validation
    if isinstance(date_input, pd.Timestamp):
        date_input = f"{date_input:%Y%m%d}"
    elif not isinstance(date_input, str):
        msg = f"finnhub error: date solver input {date_input} was not type str"
        raise Exception(msg)

    # remove whitespaces and special characters & convert strings to upper
    y = re.sub(r"[^\w\s]", '', date_input).lower()

    # solve method based on if the final element is a string i.e. in '10y'
    # otherwise we assume the input is a date string
    # there is a special case if the input is a reserved word
    if y in ["today"]:
        method = 'date_string'
    elif y[-1].isalpha():
        method = 'relative'
    else:
        method = 'date_string'

    match method:
        case 'relative':
            # freq is letter at the end; all before must be the relative period
            freq, rel = y[-1], y[:-1]

            # data validation - check rel is a numeric & freq is valid
            if freq not in ['d', 'w', 'm', 'y']:
                msg = f"date solve error: {freq} not valid freq in {y}"
                raise Exception(msg)
            elif not rel.isnumeric():
                msg = f"date solve error: {rel} not valid relative in {y}"
                raise Exception(msg)

            # datetime t1 - kept as a pd.Datetime so we can use ps.DateOffset later
            # also test if we are going end of period or not
            today = pd.to_datetime(today).date()
            if eop:
                today = end_of_period(today, freq)

            # calculated relative start date using freq & rel
            if freq == 'd':
                return today - pd.DateOffset(days=int(rel))
            elif freq == 'w':
                return today - pd.DateOffset(weeks=int(rel))
            elif freq == 'm' and eop:
                # pd.DateOffset doesn't automatically pick month end
                return today - pd.offsets.MonthEnd(n=1)
            elif freq == 'm' and not eop:
                return today - pd.DateOffset(months=int(rel))
            elif freq == 'y':
                return today - pd.DateOffset(years=int(rel))

        case 'date_string':
            try:
                return pd.to_datetime(y)
            except ValueError:
                msg = f"date solve error: {date_input} not valid input to pd.to_datetime()"
                raise Exception(msg)
