from concurrent.futures import ThreadPoolExecutor
from os import cpu_count

import numpy as np
import polars as pl
from openbb_terminal.stocks import stocks_helper as stocks
from quantstats import stats as qs


def sharpe_ratio(
    df: pl.DataFrame,
    return_column: str = "trade_return",
    N=252,
    rf=0.01,
    smart_sharpe: bool = True,
    annualize: bool = True,
    fast: bool = True,
) -> float:
    """
    Calculate the Sharpe Ratio of a return series.

    Parameters:
    -------
    * df (Series): The df to calculate the Sharpe Ratio for.
    * return_column (str): The name of the column representing the trade return.
        Defaults to "trade_return".
    * N (int, optional): The number of trading periods in a year.
        Defaults to 252.
    * rf (float, optional): The risk-free rate. Defaults to 0.01.
    * smart_sharpe (bool, optional): Whether to use the smart Sharpe Ratio.
    Defaults to True. See [link](https://www.keyquant.com/Download/GetFile?Filename=%5CPublications%5CKeyQuant_WhitePaper_APT_Part2.pdf)
    * annualize (bool, optional): Whether to annualize the Sharpe Ratio.
    Defaults to True.
    * fast (bool, optional): Whether to use the fast Sharpe Ratio.
    Defaults to True.

    Notes:
    ------
    If using `fast=True`, smart sharpe cannot be calculated. Must use fast=False
    if you want to use smart_sharpe and annualize

    Returns:
    --------
    float: The Sharpe Ratio of the return series.
    """
    if return_column not in df.columns:
        raise ValueError(f"Column {return_column} does not exist in dataframe")

    if fast is True:
        return_series = df[return_column]
        mean = return_series.mean() * N - rf
        sigma = return_series.std() * np.sqrt(N)
        return (mean / sigma).__round__(2)

    if isinstance(df, pl.DataFrame):
        df = df.to_pandas()
    out = qs.sharpe(
        returns=df[return_column],
        rf=rf,
        periods=N,
        annualize=annualize,
        smart=smart_sharpe,
    )

    return out.__round__(2)


def sortino_ratio(
    df: pl.DataFrame,
    return_column: str = "trade_return",
    N: int = 255,
    rf: float = 0.01,
    annualize: bool = True,
    smart_sortino: bool = True,
    adjusted: bool = False,
    # fast: bool = True,
):
    """
    Calculate the Sortino Ratio of a return series.

    Parameters:
    ----------
    * df (pl.Dataframe): The return series to calculate the Sortino Ratio for.
    * return_column (str): The name of the column representing the trade return.
        Defaults to "trade_return".
    * N (int, optional): The number of trading periods in a year.
        Defaults to 255.
    * rf (float, optional): The risk-free rate. Defaults to 0.01.
    * annualize (bool, optional): Whether to annualize the Sortino Ratio.
        Defaults to True.
    * smart_sortino (bool, optional): Whether to use the smart Sortino Ratio.
        Defaults to True.
    * fast (bool, optional): Whether to use the fast Sortino Ratio.
        Defaults to True. WIP

    Returns:
    --------
    float: The Sortino Ratio of the return series.

    Notes:
    -------
    See more information on Adjusted Sortino Ratio [here](https://archive.is/2rwFW)
    """
    # if fast is True:
    #     return_series = df[return_column]
    #     mean = return_series.mean() * N - rf
    #     std_neg = (return_series.filter(return_series < 0)).std() * np.sqrt(N)
    #     return mean / std_neg

    if isinstance(df, pl.DataFrame):
        df = df.to_pandas()
    if adjusted is False:
        out = qs.sortino(
            returns=df[return_column],
            rf=rf,
            periods=N,
            annualize=annualize,
            smart=smart_sortino,
        )
    elif adjusted is True:
        out = qs.adjusted_sortino(
            returns=df[return_column],
            rf=rf,
            periods=N,
            annualize=annualize,
            smart=smart_sortino,
        )

    return out.__round__(2)


def drawdown(
    df: pl.DataFrame,
    return_column: str = "trade_return",
    pct: bool = True,
    details: bool = False,
) -> float | dict:
    """
    Calculate the maximum drawdown of a return series.

    Parameters:
    df (pl.DataFrame): The DataFrame containing the return series to calculate
    the maximum drawdown for.
    return_column (str): The name of the column representing the trade return.
    Defaults to "trade_return".
    pct (bool): Whether to return the maximum drawdown in percentage.
    Defaults to True.
    details (bool): Whether to return additional details about the drawdown.
    Defaults to False.

    Returns:
    float or dict: The maximum drawdown of the return series. If details is
    True, also return the length of the drawdown in days,
    the start and end date of the maximum drawdown period.
    """
    if return_column not in df.columns:
        raise ValueError(f"Column {return_column} does not exist in dataframe")

    dd = (qs.to_drawdown_series(df[return_column].to_pandas())).__round__(6)

    # Calculate the maximum drawdown
    if pct is True:
        max_dd = (dd.min() * 100).__round__(2)
    else:
        max_dd = dd.min().__round__(4)

    if details:
        # Calculate the end index of the maximum drawdown period
        end = dd.idxmin()
        end_date = df["sell_date"][end]

        # Calculate the start of the maximum drawdown period
        peak_through_end = dd[:end]
        start = peak_through_end.idxmax()
        start_date = df["sell_date"][start]

        # Calculate the length of the maximum drawdown period
        length = (end_date - start_date).days

        return {
            "max_dd": max_dd,
            "dd_length": length,
            "dd_start_date": start_date.strftime("%Y-%m-%d"),
            "dd_end_date": end_date.strftime("%Y-%m-%d"),
        }
    else:
        return max_dd


def total_return(
    df: pl.DataFrame,
    capital_col: str = "capital",
    investment_col: str = "investment",
    pct: bool = True,
) -> float:
    tot_return = df[capital_col][-1] / df[investment_col][0] - 1

    if pct is True:
        return (tot_return * 100).__round__(2)
    else:
        return tot_return.__round__(4)


def annual_return(
    df: pl.DataFrame,
    capital_col: str = "capital",
    N: int = 365,
    pct: bool = True,
) -> float:
    """
    Calculate the average annual return in a DataFrame.

    Parameters:
    df (pl.DataFrame): The DataFrame.
    capital_col (str): The name of the column representing the capital.
    N (int, optional): The number of trading periods in a year. Defaults to 365.

    Returns:
    float: The average annual return.
    """
    # Calculate the total return
    tot_return = total_return(df, capital_col, pct=False)

    # Calculate the number of years
    years = (df["sell_date"][-1] - df["buy_date"][0]).days / N

    # Calculate the average annual return
    annual_return = (1 + tot_return) ** (1 / years) - 1
    if pct is True:
        return (annual_return * 100).__round__(2)
    else:
        return annual_return.__round__(4)


def calmar_ratio(
    df: pl.DataFrame, capital_col: str = "capital", N: int = 365
) -> float:
    """
    Calculate the Calmar ratio in a DataFrame.

    Parameters:
    df (pl.DataFrame): The DataFrame.
    capital_col (str): The name of the column representing the capital.

    Returns:
    float: The Calmar ratio.
    """
    # Calculate the average annual return
    ann_return = annual_return(df, capital_col, N, pct=False)

    # Calculate the maximum drawdownx
    max_drawdown = drawdown(df, "trade_return", pct=False, details=False)

    # Calculate the Calmar ratio
    calmar_ratio = ann_return / abs(max_drawdown)

    return calmar_ratio.__round__(2)


def treynor_ratio(
    df: pl.DataFrame,
    return_col: str = "trade_return",
    benchmark: str | pl.Series = "SPY",
) -> float:
    """
    WIP: DO NOT USE !!

    Calculate the Treynor Ratio.

    Parameters:
    df (pl.DataFrame): The DataFrame.
    return_col (str): The name of the column representing the trade return.
    beta_col (str): The name of the column representing the beta of the trade.

    Returns:
    float: The Treynor Ratio.
    """
    # Calculate the average return
    avg_return = df[return_col].mean()

    # Calculate the average beta
    if isinstance(benchmark, str):
        benchmark_data = stocks.load(
            symbol=benchmark,
            start_date=str(df["buy_date"][0]),
            end_date=str(df["sell_date"][-1]),
            verbose=False,
        )
        benchmark_returns = benchmark_data["Adj Close"].pct_change()
    elif isinstance(benchmark, pl.Series):
        benchmark_returns = benchmark["Adj Close"].pct_change()

    # Calculate the beta of the portfolio
    benchmark_returns = benchmark_returns[
        benchmark_returns.index.isin(df["sell_date"])
    ]
    matrix = np.cov(df["trade_return"], benchmark_returns)
    beta = matrix[0, 1] / matrix[1, 1]

    # Calculate the Treynor Ratio
    treynor_ratio = avg_return / beta

    return treynor_ratio.__round__(2)


# Code for trade_outcomes ------------------------------------------------------
def average_trade_duration(
    df: pl.DataFrame, buy_col: str = "buy_date", sell_col: str = "sell_date"
) -> dict:
    """
    Calculate the average, maximum, and minimum trade duration in days.

    Parameters:
    df (pl.DataFrame): The DataFrame.
    buy_col (str): The name of the column representing the buy date.
    sell_col (str): The name of the column representing the sell date.

    Returns:
    dict: A dict containing three floats. The first float is the average trade
    duration in days. The second float is the maximum trade duration in days.
    The third float is the minimum trade duration in days.
    """
    # Calculate the trade duration for each trade in days
    trade_duration_days = (df[sell_col] - df[buy_col]).dt.days()

    # Calculate the average trade duration
    avg_duration = (trade_duration_days.mean()).__round__(2)
    max_duration = trade_duration_days.max()
    min_duration = trade_duration_days.min()

    return {
        "avg_duration": avg_duration,
        "max_duration": max_duration,
        "min_duration": min_duration,
    }


def calculate_win_lose(df: pl.DataFrame, return_col: str = "trade_return"):
    total_trades = df.shape[0]
    winning_trades = df.filter(pl.col(return_col) > 0)
    num_winning_trades = winning_trades.shape[0]
    losing_trades = df.filter(pl.col(return_col) < 0)
    num_losing_trades = losing_trades.shape[0]
    winning_trades_pct = (num_winning_trades / total_trades * 100).__round__(2)
    losing_trades_pct = (num_losing_trades / total_trades * 100).__round__(2)

    return (
        total_trades,
        num_winning_trades,
        num_losing_trades,
        winning_trades_pct,
        losing_trades_pct,
    )


def calculate_biggest_trades(
    winning_trades: pl.DataFrame,
    losing_trades: pl.DataFrame,
    return_col: str = "trade_return",
):
    biggest_winning_trade = winning_trades[return_col].max() * 100
    biggest_losing_trade = losing_trades[return_col].min() * 100
    return biggest_winning_trade.__round__(2), biggest_losing_trade.__round__(2)


def calculate_qs_stats(df):
    avg_return = (qs.avg_return(df, prepare_returns=False) * 100).__round__(2)
    avg_win = (qs.avg_win(df, prepare_returns=False) * 100).__round__(2)
    avg_loss = (qs.avg_loss(df) * 100).__round__(2)
    win_loss_ratio = (qs.win_loss_ratio(df)).__round__(2)
    win_streak = qs.consecutive_wins(df)
    loss_streak = qs.consecutive_losses(df)
    return (
        avg_return,
        avg_win,
        avg_loss,
        win_loss_ratio,
        win_streak,
        loss_streak,
    )


def trade_outcomes(df: pl.DataFrame, return_col: str = "trade_return") -> dict:
    with ThreadPoolExecutor(cpu_count() - 1) as executor:
        futures = {
            "win_lose": executor.submit(calculate_win_lose, df, return_col),
            "big_trades": executor.submit(
                calculate_biggest_trades,
                df.filter(pl.col(return_col) > 0),
                df.filter(pl.col(return_col) < 0),
                return_col,
            ),
            "qs_stats": executor.submit(
                calculate_qs_stats, df[return_col].to_pandas()
            ),
        }

        results = {}
        for key, future in futures.items():
            results[key] = future.result()

    avg_trade_duration = average_trade_duration(df)

    return_dict = {
        "total_trades": results["win_lose"][0],
        "num_winning_trades": results["win_lose"][1],
        "num_losing_trades": results["win_lose"][2],
        "winning_trades_pct": results["win_lose"][3],
        "losing_trades_pct": results["win_lose"][4],
        "biggest_winning_trade": results["big_trades"][0],
        "biggest_losing_trade": results["big_trades"][1],
        "avg_trade_return": results["qs_stats"][0],
        "avg_win": results["qs_stats"][1],
        "avg_loss": results["qs_stats"][2],
        "win_loss_ratio": results["qs_stats"][3],
        "win_streak": results["qs_stats"][4],
        "loss_streak": results["qs_stats"][5],
    }

    return_dict.update(avg_trade_duration)

    return return_dict


# Code for trade_outcomes END ------------------------------------------------------


def profit_factor(df: pl.DataFrame, return_col: str = "trade_return") -> float:
    """
    Calculate the Profit Factor.

    Parameters:
    df (pl.DataFrame): The DataFrame.
    return_col (str): The name of the column representing the trade return.

    Returns:
    float: The Profit Factor.
    """
    # Calculate the sum of the positive returns
    sum_positive_returns = df.filter(pl.col(return_col) > 0)[return_col].sum()

    # Calculate the sum of the negative returns
    sum_negative_returns = df.filter(pl.col(return_col) < 0)[return_col].sum()

    # Calculate the Profit Factor
    profit_factor = sum_positive_returns / abs(sum_negative_returns)

    return profit_factor.__round__(2)


def exposure_time(
    df: pl.DataFrame,
    buy_date_col: str = "buy_date",
    sell_date_col: str = "sell_date",
    pct: bool = True,
) -> float:
    """
    Calculate the Exposure Time.

    Parameters:
    df (pl.DataFrame): The DataFrame.
    buy_date_col (str): The name of the column representing the buy date.
    sell_date_col (str): The name of the column representing the sell date.

    Returns:
    float: The Exposure Time.
    """
    # Calculate the total time invested
    total_time_invested = (df[sell_date_col] - df[buy_date_col]).sum()

    # Calculate the total time period
    total_time_period = df[sell_date_col].max() - df[buy_date_col].min()

    # Calculate the Exposure Time
    exposure_time = total_time_invested / total_time_period

    if pct is True:
        return (exposure_time * 100).__round__(2)
    else:
        exposure_time.__round__(4)


def performance_stats(
    df, return_column: str = "trade_return", melt: bool = True, **kwargs
) -> pl.DataFrame:
    """Compile trade performance statistics into a DataFrame.

    Parameters:
    df (DataFrame): DataFrame containing trade returns data
    return_column (str): Name of column in df that contains trade returns
    melt (bool): Whether to melt the output DataFrame. Default is True.
    **kwargs: Additional keyword arguments passed to underlying functions. See
    humbldata.performance.stats functions for more info on what args to pass.


    Returns:
    DataFrame: DataFrame containing performance metrics
    """

    # Setup: -------------------------------------------------------------------
    return_dict = {}

    # **kwargs used in sharpe and sortino
    N = kwargs.get("N", 252)
    rf = kwargs.get("rf", 0.01)
    annualize = kwargs.get("annualize", True)

    # Calculate Trade Stats: ---------------------------------------------------

    trade_stats = trade_outcomes(df, return_column)
    return_dict.update(trade_stats)

    # Calculate Sharpe Ratio: --------------------------------------------------
    fast = kwargs.get("fast", True)
    smart_sharpe = kwargs.get("smart_sharpe", True)
    sharpe = sharpe_ratio(
        df,
        return_column,
        N=N,
        rf=rf,
        smart_sharpe=smart_sharpe,
        annualize=annualize,
        fast=fast,
    )
    return_dict.update({"sharpe_ratio": sharpe})

    # Calculate Sortino Ratio: -------------------------------------------------
    smart_sortino = kwargs.get("smart_sortino", True)
    adjusted = kwargs.get("adjusted", False)
    sortino = sortino_ratio(
        df,
        return_column,
        N=N,
        rf=rf,
        annualize=annualize,
        smart_sortino=smart_sortino,
        adjusted=adjusted,
    )
    return_dict.update({"sortino_ratio": sortino})

    # Calculate Drawdown: ------------------------------------------------------
    drawdown_info = drawdown(df, return_column="capital", details=True)
    return_dict.update(drawdown_info)

    # Calculate Total Return: --------------------------------------------------
    tot_ret = total_return(df)
    return_dict.update({"total_return": tot_ret})

    # Calcualte Annual Return: -------------------------------------------------
    ann_ret = annual_return(df)
    return_dict.update({"annual_return": ann_ret})

    # Calculate Calmar Ratio: --------------------------------------------------
    calmar = calmar_ratio(df)
    return_dict.update({"calmar_ratio": calmar})

    # Calculate Treyor Ratio: --------------------------------------------------
    benchmark = kwargs.get("benchmark", "SPY")
    treynor = treynor_ratio(df, benchmark=benchmark)
    return_dict.update({"treynor_ratio": treynor})

    # Calculate Profit Factor: -------------------------------------------------
    profit_fact = profit_factor(df)
    return_dict.update({"profit_factor": profit_fact})

    # Calculate Exposure Time: -------------------------------------------------
    exposure = exposure_time(df)
    return_dict.update({"exposure_time": exposure})

    if melt is True:
        out = pl.DataFrame(return_dict).melt(variable_name="Metric")
    else:
        out = pl.DataFrame(return_dict)

    return out
