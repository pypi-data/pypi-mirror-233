""" Module for Anything Related to Bloomberg Calls """

# General Imports
import pandas as pd
from xbbg import blp

# Intra package imports
from hxm_refuel.jeeves import flex_date_solver
from hxm_refuel.validation import TypeHintValidation


@TypeHintValidation()
def _pdblp_freq_hack(
        call,
        t0: str,
        t1: str,
        freq: str = 'EOM'):
    """ Hack to Change Frequency of pdblp Call DataFrame """

    # pdblp defaults to outputting daily data (weekdays only)
    # We reindex based on desired frequency
    # match-case sets up required dates, then use intersection
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
    if freq.upper() in ['M', 'MONTH', 'MONTHLY', 'EOM']:
        # idx = pd.date_range(t0, t1, freq='M') + pd.offsets.MonthEnd(0)

        # first we want to subset "daily" data from call to the last date in the month
        # use a groupby function - group index by month, then filter for the max date in that group
        # https://stackoverflow.com/questions/48288059/how-to-get-last-day-of-each-month-in-pandas-dataframe-index-using-timegrouper
        idx = call.groupby(call.index.to_period('M')).apply(lambda x: x.index.max())
        call = call.reindex(index=idx)

        # now shift to the last actual day of the month
        call.index = call.index + pd.offsets.MonthEnd(0)
        return call.dropna(how='all')

    elif freq.upper() in ['W', 'WEEK', 'WEEKLY', 'W-FRI', 'FRI', 'FRIDAY']:
        idx = pd.date_range(t0, t1, freq='W-FRI')
    elif freq.upper() in ['W-THURS', 'THU', 'THURS', 'THURSDAY']:
        idx = pd.date_range(t0, t1, freq='W-THU')
    elif freq.upper() in ['W-WED', 'WED', 'WEDNESDAY']:
        idx = pd.date_range(t0, t1, freq='W-WED')
    elif freq.upper() in ['D', 'DAY', 'DAILY']:
        # https://pandas.pydata.org/docs/reference/api/pandas.bdate_range.html
        idx = pd.date_range(t0, t1, freq="B")
    elif freq.upper() in ['Y', 'YE', 'ANNUAL']:
        # want to start moving toward using resampe!!!
        return call.resample('Y').last()
    else:
        return call.dropna(how='all')

    # subset daily data using idx
    # first step here is a hack to makesure we ffill from previous day
    call = pd.concat([call, pd.DataFrame(index=idx)], axis=1)
    call = call.loc[call.index.intersection(idx), :]

    return call.dropna(how='all')


# Data Validation: ensure tickers and fields are lists and not strings
def _ticker_field_validation(x):
    """ Input Validation for Tickers & Fields
    Ensures tickers & fields are lists; dicts assume the keys are the tickers """

    if isinstance(x, list):
        return x
    elif isinstance(x, str):
        return [x]
    elif isinstance(x, dict):
        return list(x.keys())
    else:
        msg = f"bloomberg error: {x} is {type(x)}; accept types string | list | dict"
        raise ValueError(msg)


def bdp(tickers: str | list | dict = 'SPX Index',
        fields: str | list = 'PX_LAST',):
    """ Bloomberg BDP Call - Mostly a pass through from xbbg

    Args:
        tickers: str | list | dict
        fields: str | list | dict """

    # ensure ticker & fields are lists
    clean_tickers = _ticker_field_validation(tickers)
    clean_fields = _ticker_field_validation(fields)

    # make bloomberg call - NEED ERROR HANDLING
    output = blp.bdp(clean_tickers, clean_fields)

    # if input for tickers was a dict, uses values to rename tickers in output
    if isinstance(tickers, dict):
        output.index = output.index.map(tickers)

    # if dict for fields return the values from the dict as column names
    # bdp returns lower case fields so force original field tickers to lower in map
    if isinstance(fields, dict):
        output = output.rename(columns={k.lower(): v for k, v in fields.items()})

    return output


def find_yellow_buttons(tickers: list | pd.Series | pd.DataFrame):
    """ Hack to Get the Yellow Button from a ticker list

    NB/ This is a bit weird so could be unstable

    We create a dummy "unsolved" list from out input tickers, then try
    a guess at a yellow button, like "Equity". Originally used "Name" as
    the bdp field but found lots of weird things like HSBA LN accepting
    "Index". Found 2 useful fields:
        1. "parsekyable_des" which gives ZAR Curncy
        2. "parsekyable_des_source" which gives ZAR BGNL Curncy

    Use the results to update the original ticker list, and unsolved list

    Args:
        tickers: list | pd.Series | pd.DataFrame

    Returns: list """

    # want ticker in the form of a list
    # also want a duplicate as an "unsolved" list that we work on
    if isinstance(tickers, list) or isinstance(tickers, tuple):
        unsolved = tickers
    elif isinstance(tickers, pd.Series) or isinstance(tickers, pd.DataFrame):
        tickers = list(tickers.index)
        unsolved = tickers
    elif isinstance(tickers, str):
        tickers = list(tickers)
        unsolved = tickers
    else:
        raise ValueError(
            f"yellow button error: need a collection like i.e. list, tuple",
            f"or pd.Series or pd.DataFrame, where we take the index",
            f"tickers is {type(tickers)}")

    # Iterate though guessing the yellow bottom
    for guess in ["Equity", "Index", "Curncy", "Comdty", "Govt", "Corp"]:

        # append yellow button guess to list of unsolved tickers
        # try and find the Bloomberg parsekyable_des
        trial = {f"{v} {guess}": v for v in unsolved}
        results = bdp(list(trial.keys()), "parsekyable_des")

        # map index from results to remove the guess yellow key
        # convert to dict - need field_name as key to dict
        results.index = results.index.map(trial)
        results = results.to_dict()['parsekyable_des']

        # update original tickers list & drop solved tickers from unsolved list
        tickers = [results[k] if k in results.keys() else k for k in tickers]
        unsolved = [x for x in unsolved if x not in list(results.keys())]
        if len(unsolved) == 0:
            break

    return tickers


def index_member_weights(ticker: str = "UKX Index", yellow_button: bool = False):
    """ Bloomberg Index Constituents & Weights

    Args:
        ticker: str of a single ticker i.e. "UKX Index"
        yellow_button: bool [default == False] updates tickers from _yellow_button()
            - default is False because potentially call intensive to Bloomberg

    Returns: pd.Series
        - tickers (excluding yellow button) as index
        - index weight as values """

    # error handling
    try:
        # INDX_MWEIGHT call, sorted by weight with the largest on top
        # Keep the sorting here, because we use that as the trigger for the error handling
        members = blp.bds(ticker, "INDX_MWEIGHT")
        members = members.sort_values(by="percentage_weight", ascending=False)
    except KeyError:
        raise KeyError(
            f"index member weight error: {ticker} can't be sorted on 'percentage_weight',"
            f"may be a permissions problem; call looks like {members}")

    members.columns = ['ticker', 'wgts']        # Rename columns to ticker & weight
    members = members.set_index('ticker')            # set_return index as ticker

    # option to try and solve for the yellow button
    # default is no because it is quite call intensive on Bloomberg
    if yellow_button:
        members.index = find_yellow_buttons(list(members.index))

    return members.squeeze()


def index_member_and_bdp(
        ticker: str = "UKX Index",
        fields: list | tuple = ("name", "PX_LAST")):
    """ Combines Index Member Weights with BDP for Point Data

    Note: Only works if yellow_button can be found in index_member_weights; mostly Equity Indices

    Args:
        ticker: str of a single ticker i.e. "UKX Index"
        fields: list | tuple of fields to pass to BDP function

    Returns:
        pd.DataFrame with tickers as index, weights and columns from BDP
    """

    # grab index member weights with asset class key
    # feed member tickers into BDP then combine two things together
    weights = index_member_weights(ticker, yellow_button=True) / 100
    weights.index.name = "tickers"

    data = bdp(list(weights.index), fields)
    return pd.concat([weights.to_frame(), data], axis=1)


def bdh_fix_multi_index(output, tickers, fields):
    """ If BBG Output is Multi-Index & We want a Single Index """

    # need to ensure fields & tickers are wrapped in a list if they are strings
    fields = [fields] if isinstance(fields, str) else fields
    tickers = [tickers] if isinstance(tickers, str) else tickers

    if len(fields) == 1:
        # where only one field, assume caller knows what they asked for
        output.columns = output.columns.get_level_values(0).rename("")

    elif len(tickers) == 1 and len(fields) > 1:
        # where only one field, assume caller knows what they asked for
        output.columns = output.columns.get_level_values(1).rename("")

    else:
        # otherwise provide format as ticker | field
        output.columns = output.columns.map('{0[0]} | {0[1]}'.format)

    return output


@TypeHintValidation()
def bdh(tickers: str | list | dict = 'SPX Index',
        fields: str | list | dict = 'PX_LAST',
        freq: str = 'EOM',
        t0: str | pd.Timestamp = "-12m",
        t1: str | pd.Timestamp = "today",
        currency: str = None,
        multi_index: bool = False,
        interpolate: bool = True,
        ** kwargs,
        ) -> pd.DataFrame:
    """ Bloomberg BDH Call

    Requires Bloomberg API installed & pdblp 3rd party package.
    pdblp can manage overrides on fields, although we currently
    haven't built anything to manage it; test for currency didn't
    work very well which was main use case.

    INPUTS:
        tickers: list|str|dict of Bloomberg Tickers;
            if dict we assume the form {'SPX Index': 'SPX'} where keys are tickers
            function will try and rename the ticker to the value
        fields: list|str of Bloomberg Fields
        freq: Daily (default) | EOM | Weekly-Friday
        t1: end-date in str fmt YYYYMMDD; default today
        t0: start-date in str fmt YYYYMMDD; default -12m
        currency: str (default == None) mult output by XXX-FX Crncy to translate
        multi_index: True|False(default) collapses multi-index to single row
        interpolate: bool (default==True) will ffill missing data for holidays etc..
        ** kwargs are overrides one would put into your bdh formula in Excel

    SOURCE:
        https://github.com/alpha-xone/xbbg
        https://matthewgilbert.github.io/pdblp/tutorial.html
        https://www.bloomberg.com/professional/support/api-library/
    """

    clean_tickers = _ticker_field_validation(tickers)
    clean_fields = _ticker_field_validation(fields)

    # pdblp requires dates in string format of form YYYYMMDD
    # if no date provided use today and -12M
    t0 = flex_date_solver(t0).strftime("%Y-%m-%d")
    t1 = flex_date_solver(t1).strftime("%Y-%m-%d")

    try:
        call = blp.bdh(clean_tickers, clean_fields, t0, t1, **kwargs)     # Run bdh call
        call.index = pd.DatetimeIndex(call.index)                   # force datetime index
    except KeyError:
        msg = f"bloomberg error: debug needs work; check valid tickers/fields & timeseries > 3m"
        raise Exception(msg)

    # pdblp defaults to outputting daily data (weekdays only)
    # We reindex based on desired frequency
    output = _pdblp_freq_hack(call=call, t0=t0, t1=t1, freq=freq)
    output.index.name = 'date'  # worth renaming the date column while we are at it

    #
    if interpolate:
        output = output.ffill()

    # optional currency translation
    # Bloomberg's FX override is rather unstable, to we have our own
    if currency is not None:
        output = _bdh_fx_translation(output, clean_tickers, currency)

    # if input tickers came in dict format assume value is required name
    # i.e. switch out "SPX Index" to "S&P 500" in {'SPX Index': 'S&P500'}
    if isinstance(tickers, dict):
        idx = output.columns.levels[0].map(tickers)
        output.columns = output.columns.set_levels(idx, level=0)

    if isinstance(fields, dict):
        idx = output.columns.levels[1].map(fields)
        output.columns = output.columns.set_levels(idx, level=1)

    # check if we want output as multi-index or not... assume not
    if not multi_index:

        # adjust multi-index
        output = bdh_fix_multi_index(output, tickers, fields)

        return output
    else:
        return output


@TypeHintValidation()
def _bdh_fx_translation(
        prices: pd.DataFrame,
        tickers: str | list | dict,
        currency: str):
    """ Translate BDH Call Output into Different Currency

    CAUTION: Will only work for a single price based field i.e. PX_LAST

    Bloomberg's FX Override is quite unreliable and seems to frequently fail.
    Here we assume the input dataframe is prices, we use BDP to find the ticker
    currency and pull a timeseries of the FX & translate original prices.

    Args:
        prices: pd.DataFrame
        tickers: str | list | dict
        currency: str - 3 letter currency code i.e. GBP or ZAR """

    # Input validation
    if len(currency) != 3:
        msg = f"BBG FX Error: {currency} isn't a 3 letter currency code"
        raise ValueError(msg)

    # find Bloomberg currency of each ticker
    # returns dataframe with tickers as index and 1 column of currency's
    # apply map because some tickers will show, for example, GBp rather than GBP
    static = bdp(tickers, 'crncy').applymap(lambda x: x.upper())

    # find spots for currency pairs vs. requested currency
    # build as dictionary
    fx_tickers = {f"{x}{currency} Curncy": x for x in static.loc[:, 'crncy']}

    # pull FX spot rates as daily timeseries & reindex to prices index
    t0 = prices.index[0] - pd.offsets.MonthEnd(1)
    fx_rates = bdh(fx_tickers, t0=t0, t1=prices.index[-1])
    fx_rates = fx_rates.reindex(index=prices.index)

    # translate to target currency
    def _f(x, tgt_fx):

        # we find x's currency code i.e. USD from static using the ticker
        # pass if ticker is the same as target otherwise multiple through
        # may receive multi-index in which case n is a list & we want position 0
        name = x.name[0] if len(x.name) > 1 else x.name
        x_fx = static.loc[name, 'crncy']
        return x if x_fx == tgt_fx else x * fx_rates.loc[:, x_fx]

    return prices.apply(_f, args=(currency,))

# %%


# test and de-bugging space
if __name__ == "__main__":

    tickers = {"MXUS Index": "USA", "MXGB Index": "GB"}
    fields = {"PX_LAST": "Price", "PX_VOLUME": "Volume"}

    test_call = bdh(
        tickers="MXUS Index",
        fields=fields,
        t0="20030101",
        t1="20030601",
        freq='EOM',
    )

    print(test_call.tail(12))
