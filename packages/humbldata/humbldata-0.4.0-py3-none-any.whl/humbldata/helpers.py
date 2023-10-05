""" Utility functions for humbldata """
import logging

import pandas as pd
import polars as pl
from openbb_terminal.stocks import stocks_model as sm
from rich import print as prnt


class MessageHelpers:
    @staticmethod
    def log_message(msg: str, status: str, silent: bool = False):
        """
        Print a formatted and colorized message according to its status.

        Parameters
        ----------
        msg : str
            The message to print.
        status : str
            The status of the message ('success', 'info', 'warning', or 'error')
        silent : bool, optional
            If True, the function will not print the message. Default is False.

        Raises
        ------
        ValueError
            If the `status` argument is not one of 'success', 'info', 'warning',
            or 'error'.
        """

        if silent:
            return

        if status == "success":
            prnt(f"[green]:heavy_check_mark:[/green] {msg}")
        elif status == "info":
            prnt(f"[bold magenta]:information_source:[/bold magenta] {msg}")
        elif status == "warning":
            prnt(f"[yellow]:warning:[/yellow] {msg}")
        elif status == "error":
            prnt(f"[red]:x:[/red] {msg}")
        else:
            raise ValueError(
                f"Invalid status '{status}'. Expects: 'success', 'info',"
                f" 'warning', 'error'"
            )

    @staticmethod
    def get_rgb(color_name):
        """
        Get the RGB value of a color.

        Parameters
        ----------
        color_name : str
            The name of the color. Valid options are 'orange', 'lightblue',
            'yellow', 'green', and 'red'.

        Returns
        -------
        str
            The RGB value of the color as a string in the format 'rgb(x, x, x)'.

        Raises
        ------
        ValueError
            If the color_name is not one of the valid options.
        """
        # Define a dictionary that maps color names to their RGB values
        color_to_rgb: dict = {
            "orange": "rgb(255,155,0)",
            "lightblue": "rgb(50,170,230)",
            "yellow": "rgb(255,255,0)",
            "green": "rgb(10,200,10)",
            "red": "rgb(200,0,0)",
        }

        # Try to get the RGB value of the color, raise an error if the color
        # name is not valid
        try:
            return color_to_rgb[color_name]
        except KeyError as e:
            raise ValueError(
                "Invalid color name. Expected one of: 'orange', 'lightblue',"
                "'yellow', 'green', 'red'"
            ) from e


class DataStructureHelpers:
    @staticmethod
    def safe_convert_to_polars(
        df, silent: bool = True, include_index=True, lazy: bool = True
    ):
        """
        Safely converts a pandas DataFrame to a Polars DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame or polars.DataFrame
            The DataFrame to convert.
        silent : bool, optional
            If True, the function will not print the conversion message.
            Default is True.
        include_index : bool, optional
            If True, the index of the pandas DataFrame will be included in the
            conversion. Default is True.
        lazy : bool, optional
            If True, the function will return a LazyFrame. Default is True.

        Returns
        -------
        polars.DataFrame or polars.LazyFrame
            The converted DataFrame.

        Raises
        ------
        ValueError
            If the input is neither a pandas DataFrame nor a Polars DataFrame.

        Examples
        --------
        >>> safe_convert_to_polars(pd.DataFrame({"A": [1, 2], "B": [3, 4]}))
        shape: (2, 2)
        ┌─────┬─────┐
        │ A   ┆ B   │
        ├─────┼─────┤
        │ i64 ┆ i64 │
        ╞═════╪═════╡
        │ 1   ┆ 3   │
        ├─────┼─────┤
        │ 2   ┆ 4   │
        └─────┴─────┘
        """
        if isinstance(df, pl.LazyFrame):
            MessageHelpers.log_message(
                "Input is already a Pola[orange1]rs[/orange1] LazyFrame,",
                "success",
                silent,
            )
            return df

        if isinstance(df, pd.DataFrame):
            MessageHelpers.log_message(
                "Converted [dodger_blue1]pandas[/dodger_blue1] DataFrame to"
                " Pola[orange1]rs[/orange1] DataFrame...",
                "success",
                silent,
            )
            if lazy is True:
                return pl.from_pandas(df, include_index=include_index).lazy()
            else:
                return pl.from_pandas(df, include_index=include_index)
        elif isinstance(df, pl.DataFrame) and lazy is True:
            MessageHelpers.log_message(
                "Input is already a Pola[orange1]rs[/orange1] DataFrame,"
                " making lazyDataframe",
                "warning",
                silent,
            )

            return df.lazy()
        elif isinstance(df, pl.DataFrame) and lazy is False:
            MessageHelpers.log_message(
                "Input is already a Pola[orange1]rs[/orange1] DataFrame,"
                " you do not want to make it lazy...",
                "warning",
                silent,
            )

        else:
            raise ValueError(
                "Input is neither a pandas DataFrame nor a Polars DataFrame"
            )

    @staticmethod
    def convert_to_datetime(df, column, datetime: bool = False):
        """
        Converts a specified column in a DataFrame | LazyFrame to datetime or
        date format.

        Parameters
        ----------
        df : pandas.DataFrame or polars.DataFrame
            The DataFrame containing the column to convert.
        column : str
            The name of the column to convert.
        datetime : bool, optional
            If True, the function will convert the column to datetime format.
            If False, the function will convert the column to date format.
            Default is False.

        Returns
        -------
        polars.DataFrame or polars.LazyFrame
            The DataFrame with the converted column.

        Raises
        ------
        ValueError
            If the column is not of type Utf8 or Datetime.

        """
        # Setup: ---------------------------------------------------------------
        # Convert to a LazyFrame
        df = DataStructureHelpers.safe_convert_to_polars(df)

        # MAIN LOGIC -----------------------------------------------------------
        col = df.select(pl.col(column))
        if col.dtypes[0] == pl.Utf8:
            if datetime:
                df = df.with_columns(
                    pl.col(column).str.strptime(
                        pl.Datetime, "%Y-%m-%d %H:%M:%S"
                    )
                )
            else:
                df = df.with_columns(
                    pl.col(column).str.strptime(pl.Date, "%Y-%m-%d")
                )
        elif col.dtypes[0] == pl.Datetime:
            if not datetime:
                df = df.with_columns(pl.col(column).cast(pl.Date))

        return df

    @staticmethod
    def from_lazy(df: pl.DataFrame | pl.LazyFrame) -> pl.DataFrame:
        """
        Convert a LazyFrame to a DataFrame.

        Parameters
        ----------
        df : polars.LazyFrame or polars.DataFrame
            The DataFrame to convert.

        Returns
        -------
        polars.DataFrame
            The converted DataFrame.
        """
        if isinstance(df, pl.LazyFrame):
            return df.collect()
        else:
            return df


class openBBHelpers:
    @staticmethod
    def recent_price(symbol: str) -> float:
        """
        Get the most recent price for a given stock symbol.

        Parameters
        ----------
        symbol : str
            The stock symbol to get the price for.

        Returns
        -------
        float
            The most recent price for the stock symbol.
        """
        logging.getLogger("openbb_terminal.stocks.stocks_model").setLevel(
            logging.CRITICAL
        )

        data = sm.get_quote([symbol])
        price = data.loc["Price", symbol]
        return price  # type: ignore
