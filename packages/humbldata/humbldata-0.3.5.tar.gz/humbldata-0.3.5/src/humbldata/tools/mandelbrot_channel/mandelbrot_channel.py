import datetime as dt

import polars as pl
from openbb_terminal.stocks import stocks_helper as stocks

from humbldata.helpers import openBBHelpers
from humbldata.tools.mandelbrot_channel.helpers import (
    cumdev,
    cumdev_range,
    cumdev_std,
    dataset_start,
    detrend,
    log_mean,
    log_returns,
)


class MandelbrotChannel:
    """
    A class used to represent the Mandelbrot Channel.

    Attributes
    ----------
    interval : int
        The interval for the Mandelbrot Channel, default is 1440.
    prepost : bool
        A flag indicating whether to include pre and post market data,
        default is False.
    source : str
        The source of the data, default is 'YahooFinance'.
    weekly : bool
        A flag indicating whether to use weekly data, default is False.
    monthly : bool
        A flag indicating whether to use monthly data, default is False.
    verbose : bool
        A flag indicating whether to print verbose messages for openbb
        stocks.load() command, default is False.
    silent : bool
        A flag indicating whether to suppress all print statements,
        default is False.

    """

    def __init__(
        self,
        interval: int = 1440,
        prepost: bool = False,
        source: str = "YahooFinance",
        weekly: bool = False,
        monthly: bool = False,
        verbose: bool = False,
        silent: bool = False,
    ):
        self.interval = interval
        self.prepost = prepost
        self.source = source
        self.weekly = weekly
        self.monthly = monthly
        self.verbose = verbose
        self.silent = silent

    def calc_mc(
        self,
        symbol: str,
        fromdate: str | dt.datetime = "1950-01-01",
        todate: str | None = None,
        range: str = "1m",
        fast: bool = True,
    ):
        # Step 1: Collect Price Data -------------------------------------------
        # Collect todate
        if todate is None:
            todate = dt.datetime.today().strftime("%Y-%m-%d")
        # Calculate the start date
        fromdate = dataset_start(
            range=range, fromdate=fromdate, todate=todate, return_dt=False
        )
        # Collect Price
        price_df = stocks.load(
            symbol=symbol,
            start_date=fromdate,
            end_date=todate,
            interval=self.interval,
            prepost=self.prepost,
            source=self.source,
            weekly=self.weekly,
            monthly=self.monthly,
            verbose=self.verbose,
        )[["Adj Close"]]
        price_df = pl.from_pandas(price_df, include_index=True).lazy()

        # Step 2: Calculate Log Returns ----------------------------------------
        price_df = log_returns(df=price_df)

        # Step 3: Calculate Log Mean Series ------------------------------------
        log_mean_df = log_mean(df=price_df, range=range)

        # Step 4: Calculate Mean De-trended Series -----------------------------
        # Creates a merged dataframe with price_df data, and detrended mean
        out_df = detrend(df=price_df, mean_df=log_mean_df)

        # Step 5: Calculate Cumulative Deviate Series --------------------------
        out_df = cumdev(df=out_df)

        # Step 6: Calculate Mandelbrot Range -----------------------------------
        R = cumdev_range(df=out_df)

        # Step 7: Calculate Standard Deviation ---------------------------------
        S = cumdev_std(df=out_df)

        # Step 8: Calculate Rescaled Range -------------------------------------
        RS = pl.Series("RS", R / S)
        RS_mean = RS.mean()
        RS_max = RS.max()
        RS_min = RS.min()

        # Step 9: Calculate Rescaled Price Range -------------------------------
        if fast:
            recent_price = (
                out_df.select(pl.col("Adj Close")).last().collect().rows()[0][0]
            )
        else:
            recent_price = openBBHelpers.recent_price("AAPL")

        # STD of the last range od detrended_mean?
        price_range_mean = RS_mean * np.std() * recent_price

        return out_df


#### R DIRECT TRANSLATION ======================================================
from datetime import datetime

import numpy as np
import pandas as pd
from scipy.stats import tstd
from yfinance import download


def rescaled_range(
    symbol=None,
    range=None,
    start_date=None,
    end_date=None,
    interval=1440,
    prepost=False,
    source="yahoo",
    weekly=None,
    monthly=None,
    verbose=None,
    silent=False,
    plot=False,
):
    # Log
    print("calculating rescaled_range()")

    # DEFENSIVES ---------------------------------------------------------------
    # Assert stock symbol
    symbol = symbol.upper()
    assert len(symbol) >= 2, "<symbol> name was too short"
    assert len(symbol) <= 10, "<symbol> name was too long"

    # Assert range
    assert len(range) >= 2, "<range> was too short"

    # Assert `start_date` and `end_date`
    if start_date is not None:
        start_date = pd.to_datetime(start_date)
    if end_date is not None:
        end_date = pd.to_datetime(end_date)

    # END DEFENSIVES------------------------------------------------------------

    # 1: PRICE COLLECTION-------------------------------------------------------
    if not silent:
        print("Step 1: Collecting Dates...")

    # Collect Price
    symbol_ts = download(
        symbol,
        start=start_date,
        end=end_date,
        interval=interval,
        prepost=prepost,
    )

    # Check symbol_ts is equal to range_needed_1
    assert (
        symbol_ts.shape[0] == range_needed_1
    ), "DataFrame rows not equal to range_needed_1"
    assert symbol_ts.shape[1] == 9, "DataFrame columns not equal to 9"

    # 2: LOG RETURN SERIES------------------------------------------------------
    if not silent:
        print("Step 3: Calculating log return series...")

    # create daily log returns
    symbol_ts["log.returns"] = np.log(symbol_ts["Adj Close"]).diff()
    symbol_ts["log.returns_pct"] = symbol_ts["log.returns"] * 100

    # Assert the Date column is in order
    assert (
        symbol_ts.index.is_monotonic_increasing
    ), "<date> column was returned out of order"

    # 3: LOG MEAN SERIES--------------------------------------------------------
    if not silent:
        print("Step 4: Calculating log mean series...")

    # Get the number of 'ranges' available in the data
    range_num = range_needed / range_width

    # Create a sequence of 'ranges'
    range_seq = np.arange(1, range_num + 1, 1)

    # Calculate the log mean
    log_mean = symbol_ts["log.returns"].rolling(window=range_width).mean()

    # 4: MEAN DETRENDED SERIES--------------------------------------------------
    if not silent:
        print("Step 5: Calculating detrended series...")

    # Split the log mean series at range_width breaks
    log_split = np.array_split(symbol_ts["log.returns"], range_seq)

    # Remove the mean from the log mean series (detrending)
    log_split_mean_rm = [x - y for x, y in zip(log_split, log_mean)]

    # 5: CUMDEV SUM SERIES------------------------------------------------------
    if not silent:
        print("Step 6: Calculating cumulative deviate series...")

    # Create cumulative deviate series
    cum_dev = [np.cumsum(x) for x in log_split_mean_rm]

    # Check validity of calculation
    cum_dev_check = [x[-1] for x in cum_dev]
    assert all(
        x == 0 for x in cum_dev_check
    ), "cumulative deviate series does not end in 0, a correct calculation should have a mean of 0"

    # 6: EXTRACT RANGE----------------------------------------------------------
    if not silent:
        print("Step 7: Calculating range statistics...")

    # Extract highest range value
    range_hi = [np.max(x) for x in cum_dev]

    # Extract lowest range value
    range_lo = [np.min(x) for x in cum_dev]

    # Calculate the range: hi - lo
    R = [hi - lo for hi, lo in zip(range_hi, range_lo)]

    # 7: CALCULATE STD SERIES---------------------------------------------------
    if not silent:
        print("Step 8: Calculating standard deviation...")

    S = [tstd(x) for x in log_split]

    # 8: CALCULATE RESCALED STATISTICS------------------------------------------
    # The hurst-mandelbrot R/S is the rescaled return in STD's, we need to
    # convert that back into a price unit

    if not silent:
        print("Step 9: Calculating rescaled range...")

    # RS[i] = return range in STD per range in ts
    RS = [r / s for r, s in zip(R, S)]

    # calculate price range from rescaled return above
    RS_mean = np.mean(RS)
    np.ptp(RS)
    RS_min = np.min(RS)
    RS_max = np.max(RS)

    # Logic to calculate rescaled price range
    # RS * sd()
    # convert to range of returns} * last_close price {convert to $ unit}
    recent_price = symbol_ts["Adj Close"].iloc[-1]

    # Caculate the price range/mean/min/max
    (
        RS_mean
        * np.std(log_split_mean_rm[range_num - 1])
        * symbol_ts["Adj Close"].iloc[-1]
    )
    (
        RS_min
        * np.std(log_split_mean_rm[range_num - 1])
        * symbol_ts["Adj Close"].iloc[-1]
    )
    (
        RS_max
        * np.std(log_split_mean_rm[range_num - 1])
        * symbol_ts["Adj Close"].iloc[-1]
    )
    price_range = (
        RS[range_num - 1]
        * np.std(log_split_mean_rm[range_num - 1])
        * symbol_ts["Adj Close"].iloc[-1]
    )

    # Calculate the current price range/mean/min/max
    current_range = (
        RS[range_num - 1]
        * np.std(log_split_mean_rm[range_num - 1])
        * recent_price
    )
    (RS_max * np.std(log_split_mean_rm[range_num - 1]) * recent_price)
    (RS_min * np.std(log_split_mean_rm[range_num - 1]) * recent_price)
    (RS_mean * np.std(log_split_mean_rm[range_num - 1]) * recent_price)

    # Relative position modifier ()
    pos_modify_hi = range_hi[range_num - 1] / (
        range_hi[range_num - 1] - range_lo[range_num - 1]
    )
    pos_modify_lo = range_lo[range_num - 1] / (
        range_hi[range_num - 1] - range_lo[range_num - 1]
    )

    price_range * pos_modify_hi
    current_top = current_range * pos_modify_hi

    price_range * pos_modify_lo
    current_bottom = current_range * pos_modify_lo

    top_range = symbol_ts["Adj Close"].iloc[-1] + current_top
    bottom_range = symbol_ts["Adj Close"].iloc[-1] + current_bottom

    # 9: EXPORT STATS-----------------------------------------------------------
    if not silent:
        print("Exporting data...")

    # Table to return
    out_table = pd.DataFrame(
        {
            "symbol": [symbol],
            "date": [datetime.now()],
            "range": [range],
            "bottomRange": [bottom_range],
            "lastPrice": [recent_price],
            "topRange": [top_range],
        }
    )

    print(
        f"{range} Mandelbrot Channel: \n Symbol: {symbol} \n Date: {datetime.now()} \n Bottom Range: {bottom_range} -- Last Price: {recent_price} -- Top Range: {top_range}"
    )

    return out_table
