import datetime as dt

import polars as pl
from openbb_terminal.stocks import stocks_helper as stocks

from humbldata.helpers import MessageHelpers, openBBHelpers
from humbldata.tools.mandelbrot_channel.helpers import (
    cumdev,
    cumdev_range,
    cumdev_std,
    dataset_start,
    detrend,
    log_mean,
    log_returns,
    price_range,
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
        RS_method: str = "RS",
        fast: bool = True,  # uses price from first stock data collection vs grabbing the most recent price
        silent: bool = True,
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
        R, range_max, range_min = cumdev_range(df=out_df)

        # Step 7: Calculate Standard Deviation ---------------------------------
        S = cumdev_std(df=out_df)

        # Step 8: Calculate Rescaled Range -------------------------------------
        RS = pl.Series("RS", R / S)
        if not fast:
            RS_mean = RS.mean()  # noqa: F841
            RS_max = RS.max()  # noqa: F841
            RS_min = RS.min()  # noqa: F841

        # Step 9: Calculate Rescaled Price Range -------------------------------
        if fast:
            recent_price = (
                out_df.select(pl.col("Adj Close")).last().collect().rows()[0][0]
            )
        else:
            recent_price = openBBHelpers.recent_price(symbol)  # noqa: F841


        self.top_price, self.bottom_price = price_range(
            df=out_df,
            fast=fast,
            RS=RS,
            RS_mean=RS_mean if not fast else None,
            RS_max=RS_max if not fast else None,
            RS_min=RS_min if not fast else None,
            recent_price=recent_price,
            range_max=range_max,
            range_min=range_min,
            RS_method=RS_method,
        )

        if not fast and not silent:
            # Create the message
            MessageHelpers.log_message(
                f"'[deep_sky_blue1]{range}[/deep_sky_blue1]' Mandelbrot Channel:\n Symbol: [green]{symbol}[/green] \n Date: [green]{dt.datetime.now()}[/green] \n Bottom Range: [green]{bottom_price}[/green] -- Last Price: [green]{recent_price}[/green] -- Top Range: [green]{top_price}[/green]",
                "success",
            )

        return self

