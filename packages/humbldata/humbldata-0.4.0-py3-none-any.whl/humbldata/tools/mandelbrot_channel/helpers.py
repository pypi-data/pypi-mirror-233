"""
This is a helper file for MandelbrotChannel tools.
"""
import datetime as dt
import math

import polars as pl

from humbldata.helpers import DataStructureHelpers


def _range_days(
    range: str | None = None,
    fromdate: str | dt.datetime | None = None,
    todate: str | dt.datetime | None = None,
) -> tuple:
    """
    This function calculates the number of days in a given range or between two
    dates.

    Parameters
    ----------
    range : str, optional
        The range to calculate the number of days for. The range should be a
        string containing a number followed by a period identifier
        ('d' for days, 'w' for weeks,'m' for months, 'q' for quarters, or 'y'
        for years). For example, '2w' represents two weeks, which is 14 days.
    fromdate : str or datetime.datetime, optional
        The start date to calculate the number of days from. If a string is
        provided, it should be in the format 'YYYY-MM-DD'.
    todate : str or datetime.datetime, optional
        The end date to calculate the number of days to. If a string is
        provided, it should be in the format 'YYYY-MM-DD'.

    Returns
    -------
    tuple
        The number of days in the given range or between the two dates.
        Returns fromdate and todate, if they are provided.

    Raises
    ------
    ValueError
        If an invalid range is provided.
    """
    if fromdate and todate:
        fromdate = (
            dt.datetime.strptime(fromdate, "%Y-%m-%d")
            if isinstance(fromdate, str)
            else fromdate
        )
        todate = (
            dt.datetime.strptime(todate, "%Y-%m-%d")
            if isinstance(todate, str)
            else todate
        )
        return ((todate - fromdate).days), fromdate, todate

    if range:
        range_periods = {"d": 1, "w": 7, "m": 30.4, "q": 91, "y": 365.25}
        for period, days in range_periods.items():
            if period in range:
                num_periods = int(range.split(period)[0])
                return num_periods * days, None, None

    raise ValueError(
        "Invalid range. Please use 'd' for days, 'w' for weeks, 'm' for months, 'q' for quarters, or 'y' for years."
    )


def _range_format(range_str: str) -> str:
    """
    This function formats a range string into a standard format.

    Parameters
    ----------
    range_str : str
        The range string to format. It should contain a number followed by a
        range part. The range part can be 'day', 'week', 'month', 'quarter', or
        'year'. The range part can be in singular or plural form and can be
        abbreviated. For example, '2 weeks', '2week', '2wks', '2wk', '2w' are
        all valid.

    Returns
    -------
    str
        The formatted range string. The number is followed by an abbreviation of
        the range part ('d' for day, 'w' for week, 'mo' for month, 'q' for
        quarter, 'y' for year). For example, '2 weeks' is formatted as '2w'.

    Raises
    ------
    ValueError
        If an invalid range part is provided.
    """
    range_dict = {
        "day": "d",
        "week": "w",
        "month": "mo",
        "quarter": "q",
        "year": "y",
    }

    # Check if a space exists in the string
    if " " in range_str:
        # Split the input string into number and range part
        num, range_part = range_str.split()
    else:
        # Separate the number and range part
        num = "".join(filter(str.isdigit, range_str))
        range_part = "".join(filter(str.isalpha, range_str))

    # Remove any non-alphabetic characters from the range part
    range_part = "".join(filter(str.isalpha, range_part))

    # Remove trailing 's' if it exists (for plural forms)
    if range_part.endswith("s"):
        range_part = range_part[:-1]

    # Find the abbreviation for the range part in the dictionary
    for key in range_dict.keys():
        if key.startswith(range_part):
            range_part = range_dict[key]
            break

    # Return the formatted range string
    return num + range_part


def dataset_start(
    range: str | None = None,
    fromdate: str | dt.datetime | None = None,
    todate: str | dt.datetime | None = None,
    return_dt: bool = False,
) -> str | dt.datetime:
    """
    This function calculates the start date of the dataset based on the range,
    fromdate, and todate. The purpose is to ensure that the total width of the
    dates encompasses an integer number of range widths. If necessary, the
    function extends the start date to accommodate an additional range width.

    Parameters
    ----------
    range : str | None, optional
        The range of the dataset. It can be 'd' for days, 'w' for weeks, 'm'
        for months, 'q' for quarters, or 'y' for years.
    fromdate : str | dt.datetime | None, optional
        The start date of the dataset.
    todate : str | dt.datetime | None, optional
        The end date of the dataset.
    return_dt : bool, optional
        If True, the function will return the start date as a datetime object.
        If False, the function will return the start date as a string.

    Returns
    -------
    str | dt.datetime
        The start date of the dataset to collect price data from.
    """
    if range is None or fromdate is None or todate is None:
        raise ValueError("Range, fromdate, and todate cannot be None.")

    try:
        range_width = _range_days(range=range)[
            0
        ]  # ignore None's in tuple from _range_days
        total_width, fromdate, todate = _range_days(
            fromdate=fromdate, todate=todate
        )
        width_needed = math.ceil(total_width / range_width) * range_width
        start_date = todate - dt.timedelta(days=width_needed)  # type: ignore
        if return_dt:
            return start_date
        else:
            return start_date.strftime("%Y-%m-%d")
    except ZeroDivisionError as d:
        raise ValueError("Range width cannot be zero.") from d
    except Exception as e:
        raise ValueError(
            "An error occurred while calculating the start date: " + str(e)
        ) from e


def log_returns(
    df: pl.DataFrame | pl.LazyFrame, column_name: str = "Adj Close"
) -> pl.DataFrame | pl.LazyFrame:
    """
    This function calculates the log returns of a given column in a DataFrame.

    Parameters
    ----------
    df : pl.DataFrame | pl.LazyFrame
        The DataFrame or LazyFrame to calculate log returns on.
    column_name : str, optional
        The name of the column to calculate log returns on. Default is "Adj Close".

    Returns
    -------
    pl.DataFrame | pl.LazyFrame
        The DataFrame or LazyFrame with a new column "log_returns" added, which contains the log returns of the specified column.
    """
    df = df.set_sorted("date")

    return df.with_columns(
        pl.col(column_name).log().diff().alias("log_returns")
    ).drop_nulls(subset="log_returns")


def log_mean(
    df: pl.DataFrame | pl.LazyFrame, range: str
) -> pl.DataFrame | pl.LazyFrame:
    """
    This function calculates the rolling mean of 'log_returns' in a DataFrame or LazyFrame.

    Parameters
    ----------
    df : pl.DataFrame | pl.LazyFrame
        The DataFrame or LazyFrame to calculate the rolling mean on.
    range : str
        The range to calculate the rolling mean over.

    Returns
    -------
    pl.DataFrame | pl.LazyFrame
        The DataFrame or LazyFrame with a new column "log_mean" added, which contains the rolling mean of 'log_returns'.
    """
    df = df.set_sorted("date")

    df = df.group_by_dynamic(
        "date", every=_range_format(range), closed="left", check_sorted=False
    ).agg([pl.col("log_returns").mean().alias("log_mean")])

    return df


def get_date_range(df: pl.DataFrame | pl.LazyFrame, index: int) -> tuple:
    """
    This function retrieves the start and end dates for a given range in a
    DataFrame or LazyFrame.

    Parameters
    ----------
    df : pl.DataFrame | pl.LazyFrame
        The DataFrame or LazyFrame to retrieve the date range from.
    index : int
        The index of the range to retrieve the dates for.

    Returns
    -------
    tuple
        A tuple containing the start and end dates for the range. The end date
        is None if the range is the last one in the DataFrame or LazyFrame.
    """
    df = DataStructureHelpers.from_lazy(df)
    start_date = df["date"][index]
    end_date = df["date"][index + 1] if index + 1 < df.shape[0] else None
    return start_date, end_date


def detrend(
    df: pl.DataFrame | pl.LazyFrame,
    mean_df: pl.DataFrame | pl.LazyFrame,
    sort: bool = False,
) -> pl.LazyFrame:
    """
    Detrends a DataFrame by subtracting the mean of each range.

    - Adds column `detrended_mean`
    - Adds column `range_n`: the nth range

    Parameters
    ----------
    df : pl.DataFrame | pl.LazyFrame
        The DataFrame or LazyFrame to detrend.
    mean_df : pl.DataFrame | pl.LazyFrame
        The DataFrame or LazyFrame containing the means for each range.
    sort : bool, optional
        If True, sorts both DataFrames by date before detrending.
        Default is False.

    Returns
    -------
    pl.DataFrame
        The detrended DataFrame.

    Examples
    --------
    >>> df = pl.DataFrame({
    ...     "date": pd.date_range(start="2020-01-01", end="2020-12-31"),
    ...     "log_returns": np.random.normal(size=366)
    ... })
    >>> mean_df = log_mean(df, range="1m")
    >>> detrended_df = mean_detrend(df, mean_df)
    """
    # Ensure both DataFrames are sorted by date
    if sort:
        df = df.sort("date")
        mean_df = mean_df.sort("date")

    df = DataStructureHelpers.from_lazy(df)
    mean_df = DataStructureHelpers.from_lazy(mean_df)

    # Initialize a list to store the detrended values
    # Initialize an empty DataFrame
    detrended_df = pl.DataFrame(
        {
            "date": pl.Series("date", [], dtype=pl.Datetime(time_unit="ns")),
            "detrended_mean": pl.Series("detrended_mean", [], dtype=pl.Float64),
            "range_n": pl.Series("range_n", [], dtype=pl.UInt16),
        }
    )

    # Iterate over the ranges in mean_df
    for i in range(mean_df.shape[0]):
        # Get the start and end dates for the current range
        start_date, end_date = get_date_range(mean_df, i)

        # Get the mean for the current range
        mean = mean_df["log_mean"][i]

        # Get the values in df that fall within the current range
        if end_date is not None:
            values = df.filter(
                (pl.col("date") >= start_date) & (pl.col("date") < end_date)
            ).select(pl.col("*").exclude("Adj Close"))
        else:
            values = df.filter(pl.col("date") >= start_date).select(
                pl.col("*").exclude("Adj Close")
            )

        # Create a DataFrame with the detrended values and the corresponding dates
        new_df = pl.DataFrame(
            {
                "date": values["date"],
                "detrended_mean": values["log_returns"] - mean,
                "range_n": pl.Series([i] * values.shape[0]).cast(pl.UInt16),
            }
        )
        # Append the new DataFrame to detrended_df
        detrended_df = detrended_df.vstack(new_df)

    merged_df = df.join(detrended_df, on="date", how="left")

    return merged_df.lazy()


def cumdev(df: pl.DataFrame | pl.LazyFrame, column: str = "detrended_mean"):
    """
    Calculate the cumulative deviate series of a column in a DataFrame.

    Parameters
    ----------
    df : pl.DataFrame
        The DataFrame to process.
    column : str
        The name of the column to calculate the cumulative deviate series for.

    Returns
    -------
    pl.DataFrame
        The DataFrame with the cumulative deviate series added as a new column.
    """
    # Calculate the cumulative sum of the column

    df = df.with_columns(pl.col(column).cumsum().alias("cumdev"))

    _cumdev_check(df, column="cumdev")
    return df


def _cumdev_check(df: pl.DataFrame | pl.LazyFrame, column: str = "cumdev"):
    """
    Check if the last value of a column in a DataFrame is 0.

    Parameters
    ----------
    df : pl.DataFrame
        The DataFrame to check.
    column : str
        The name of the column to check.

    Raises
    ------
    AssertionError
        If the last value of the column is not 0.
    """
    from numpy import isclose

    # Get the last value of the column
    if isinstance(df, pl.DataFrame):
        value = df[column].tail(1)[0]
    else:
        value = df.collect()[column].tail(1)[0]
    # Assert that the last value is 0
    assert isclose(
        value, 0, atol=1e-6
    ), f"The value is not close to 0, it's {value}"


def cumdev_range(
    df: pl.DataFrame | pl.LazyFrame, column: str = "cumdev"
) -> tuple[pl.Series, pl.Series, pl.Series]:
    """
    Calculate the range (max - min) of a specified column in a DataFrame.

    Parameters
    ----------
    df : pl.DataFrame
        The DataFrame to calculate the range from.
    column : str, optional
        The column to calculate the range from, by default "cumsum".

    Returns
    -------
    float
        The range of the specified column.
    """
    range_df = df.group_by("range_n").agg(
        [
            pl.col(column).min().alias("min"),
            pl.col(column).max().alias("max"),
        ]
    )

    range_df = range_df.sort("range_n").collect()  # type: ignore

    range_series = pl.Series("R", range_df["max"] - range_df["min"])

    return range_series, range_df["max"], range_df["min"]


def cumdev_std(
    df: pl.DataFrame | pl.LazyFrame, column: str = "cumdev"
) -> pl.Series:
    """
    Calculate the standard deviation of a specified column in a DataFrame for
    each range.

    Parameters
    ----------
    df : pl.DataFrame
        The DataFrame to calculate the standard deviation from.
    column : str, optional
        The column to calculate the standard deviation from, by default "cumdev".

    Returns
    -------
    pl.Series
        The series of standard deviations for the specified column.
    """
    std_df = df.group_by("range_n").agg(
        [
            pl.col(column).std().alias("S"),
        ]
    )

    std_df = std_df.sort("range_n").collect()  # type: ignore

    std_series = pl.Series("S", std_df["S"])

    return std_series


def price_range(
    df: pl.LazyFrame | pl.DataFrame,
    fast: bool = True,
    RS: pl.Series | None = None,
    RS_mean: float | None = None,
    RS_max: float | None = None,
    RS_min: float | None = None,
    recent_price: float | None = None,
    range_max: pl.DataFrame | None = None,
    range_min: pl.DataFrame | None = None,
    RS_method: str = "RS",
    **kwargs,
) -> tuple[float, float]:
    # Check if RS_method is one of the allowed values
    if RS_method not in ["RS", "RS_mean", "RS_max", "RS_min"]:
        raise ValueError(
            "RS_method must be one of 'RS', 'RS_mean', 'RS_max', 'RS_min'"
        )

    # Convert df
    df = DataStructureHelpers.from_lazy(df)

    # Extract the latest detrended Return Series
    STD_detrended_mean = (
        df.filter(pl.col("range_n") == pl.col("range_n").max())
        .select(pl.col("detrended_mean"))
        .to_series()
        .std()
    )
    # Calculate price_range using the last range's statistics
    if RS_method == "RS":
        price_range = (
            RS.tail(1)[0] * STD_detrended_mean * recent_price
        )  # noqa: F841
    elif RS_method == "RS_mean":
        price_range = RS_mean * STD_detrended_mean * recent_price  # noqa: F841
    elif RS_method == "RS_max":
        price_range = RS_max * STD_detrended_mean * recent_price  # noqa: F841
    elif RS_method == "RS_min":
        price_range = RS_min * STD_detrended_mean * recent_price  # noqa: F841

    # Relative Position Modifier
    top_modifier = range_max.tail(1)[0] / (
        range_max.tail(1)[0] - range_min.tail(1)[0]
    )
    bottom_modifier = range_min.tail(1)[0] / (
        range_max.tail(1)[0] - range_min.tail(1)[0]
    )

    top = price_range * top_modifier  # noqa: F841
    bottom = price_range * bottom_modifier  # noqa: F841

    top_price = round(recent_price + top, 3)  # noqa: F841
    bottom_price = round(recent_price + bottom, 3)  # noqa: F841

    return top_price, bottom_price
