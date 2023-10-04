# -*- coding: utf-8 -*-
""" Bloomberg Recipes
Collection of functions which use the Bloomberg API to do something useful
"""

import pandas as pd
from hxm_refuel.bloomberg import bdh, bdp


def bbg_cape(
        ticker: str = "SPX Index",
        inflation: str | None = None,
        w=120,
        full=False):
    """ Quick Calculation of CAPE using a Total Return Series & Inflation Ticker

    Shiller's Cyclically Adjusted Price/Earnings (CAPE) Ratio calling from Bloomberg API.
    Quick & dirty, calls from BBG for each series; don't use if you have data already.

    If inflation ticker missing, we will try and match inflation using the FX code of the
    equity index provided; supports USD, ZAR, EUR, GBP, JPY and default to USD if missing.

    Note, Shiller PE is PX_t / RealAvgEPS_(t-1) but that is a faff so we use t for both

    Args:
        ticker: str: Bloomberg equity ticker i.e. "SPX Index"
        inflation: str | None (default): ticker of inflation index; NOT YoY
            - will attempt to find inflation based on equity index FX code if None
        w: int = 120: number of periods to use for EPS averaging
        full: Boolean (default == False) shows all data rather than just cape in return

    Reference:
        - http://www.econ.yale.edu/~shiller/data.htm

    """

    # equity data from Bloomberg
    fields = ["PX_LAST", "TRAIL_12M_EPS"]
    equity = bdh(ticker, fields=fields, t0="-100y").dropna()
    equity.columns = ["px", "eps"]

    # options if no inflation series passes
    if inflation is None:
        # some inflation defaults by currency
        cpi_dict = {
            "USD": "CPI Index",
            "ZAR": "SACPI Index",  # starts in 1980
            "EUR": "ECCPEMUY Index",  # starts 1997
            "GBP": "UKRPI Index",  # starts 1987 but is RPI not CPI
            "JPY": "JNCPI Index",  # starts in 1970s
        }

        fx = bdp("SPX Index", "crncy").squeeze().upper()
        fx = fx if fx in cpi_dict.keys() else "USD"
        inflation = cpi_dict[fx]

    # pull inflation series from Bloomberg and create deflator series
    # follow Shiller's method and have deflator as a multiplier: cpi_t / cpi_(t-i)
    cpi = bdh(inflation, t0=equity.index[0]).squeeze().rename("inflation")
    deflator = (cpi.iloc[-1] / cpi).rename("deflator")

    # create series of real prices & real earnings
    real = equity.apply(lambda x: x * deflator).rename(columns={"px": "real_px", "eps": "real_eps"})
    avg_eps = real.iloc[:, 1].rolling(window=w).mean().rename("avg_eps")  # rolling real eps
    cape = (real.iloc[:, 0] / avg_eps).rename("cape")  # cape = real_px / real_avg_eps

    # by default, we don't show all the workings
    if full:
        return pd.concat([cape, equity, cpi, deflator, real, avg_eps], axis=1)
    else:
        return cape.dropna().rename(ticker)
