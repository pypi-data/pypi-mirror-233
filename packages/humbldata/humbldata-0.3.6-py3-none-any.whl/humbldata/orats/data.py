""" This module contains the functions to pull data from ORATS data service"""

import json
from datetime import date

import pandas_market_calendars as mcal
import polars as pl
import requests
from humbldata.constants import IV_ENDPOINTS, ORATS_BASE_URL, ORATS_ENDPOINTS
from humbldata.credentials import APICredentials
from humbldata.helpers import MessageHelpers as msg


class OratsData:
    """
    The set of functions to pull data from ORATS Option data:
    (https://www.orats.com/)
    """

    def __init__(self, token: str = None, silent: bool = False) -> None:
        """
        Initialize an OratsData Object.

        Parameters
        ----------
        token : str
            The API credential to get from ORATS
        silent : bool, optional
            If True, the function will NOT print messages. Default is False.
        """

        if token is None:
            self.token = APICredentials().get_orats()
        else:
            self.token = token
        self.silent: bool = silent

    def check_orats_endpoints(self, value):
        """
        This method checks if the provided value is a valid key in the
        ORATS_ENDPOINTS dictionary.

        Parameters:
        ----------
        self : object
            An instance of the class where this method is defined.
        value : str
            The key to be checked in the ORATS_ENDPOINTS dictionary.

        Raises:
        ------
        ValueError:
            If the provided value is not found in ORATS_ENDPOINTS dictionary.

        Returns:
        -------
        None
        """
        try:
            ORATS_ENDPOINTS[value]
        except KeyError as exc:
            raise ValueError(
                f"'{value}' is not a valid ORATS_ENDPOINTS value"
            ) from exc

    def get_data(
        self,
        endpoint: str,  # required argument
        ticker: str,  # required argument
        fromdate: str = None,
        todate: str = None,
        fields: list[str] = None,
        dte: list[int] = None,
        delta: list[float] = None,
        tradedate: str = None,
        strikes: int = None,
        symbols: list[str] = None,
        expirdate: str = None,
    ) -> pl.DataFrame | None:
        """
        Get historical data through ORATS API (https://api.orats.io/datav2) and
        more information could found at https://docs.orats.io/data-api-guide/

        Parameters
        ----------
        - endpoint : str
            The supported api methods, such as `strikes`
        - ticker : str
            The supported underlying assets' tickers, such as `AAPL`
        - fromdate : str
            Format as `YYYY-MM-DD`
        - todate : str, optional
            Format as `YYYY-MM-DD`
        - fields : list[str], optional
            If given, only given fields will be pulled from API, this would
            be useful if requried data size is large. By default, all fields
            are pulled.
        - dte : list[int], optional
            A list of days to expiration. Data will be subset between the values
            If provided, only given days to
            expiration will be pulled.
        - delta : list[float], optional
            A list of delta values to subset between.
            If provided, only given delta will be pulled.
        - dates : list[str], optional
            A list of 'YYYY-MM-DD' dates. If provided, only given dates will
            be pulled and `fromdate`, `todate` will be ignored.
        - strike : int, optional
            The strike price to pull data from.  Used with endpoint
            strikesHistoryByOptions.
        - symbols : list[str], optional
            A list of OCC ption symbols or underlying symbols. Used with
            endpoint strikesByOptions.
        - expirdate : str, optional
            The expiration date to pull data from. Used with endpoint
            strikesHistoryByOptions.


        Returns
        -------
        pandas.DataFrame or Dict{str: pd.DataFrame}
            The returned values from ORATS per day
        """
        # Setup Messaging ----
        m = msg.log_message

        # Step 1: Check Endpoint
        self.check_orats_endpoints(value=endpoint)

        # Step 2: Set Market Calender (adjust expirDate/tradeDate)
        if expirdate is not None:
            nyse = mcal.get_calendar("NYSE")
            expirdate = nyse.valid_days(
                start_date="2007-01-03", end_date=expirdate
            )[-1].strftime("%Y-%m-%d")
            # Messaging
            m(
                msg="<expirdate> modified to: " + expirdate,
                status="info",
                silent=self.silent,
            )
        if tradedate is not None:
            nyse = mcal.get_calendar("NYSE")
            tradedate = nyse.valid_days(
                start_date="2007-01-03", end_date=tradedate
            )[-1].strftime("%Y-%m-%d")
            # Messaging
            m(
                msg="<tradedate> modified to: " + tradedate,
                status="info",
                silent=self.silent,
            )

        # Step 3: Use internal fct to get data
        if endpoint not in IV_ENDPOINTS:
            data = self._get_data(
                endpoint=endpoint,
                ticker=ticker,
                fromdate=fromdate,
                todate=todate,
                tradedate=tradedate,
                dte=dte,
                delta=delta,
                fields=fields,
            )
        elif endpoint in IV_ENDPOINTS:
            data = self._get_data_ivol(
                endpoint=endpoint,
                ticker=ticker,
                fromdate=fromdate,
                todate=todate,
                tradedate=tradedate,
                dte=dte,
                delta=delta,
            )

        if data is None:
            # Messaging
            m(
                msg=f"[orange1]ORATS[/orange1] [bright_yellow]{endpoint}"
                f"[/bright_yellow] request for [bsteel_blue1]{ticker} "
                f"[/bsteel_blue1]failed...",
                status="error",
                silent=self.silent,
            )
        else:
            m(
                msg=f"[orange1]ORATS[/orange1] [bright_yellow]{endpoint}"
                f"[/bright_yellow] request for [bsteel_blue1]{ticker}"
                f"[/bsteel_blue1] succeeded!",
                status="success",
                silent=self.silent,
            )
        return data

    def _get_data(
        self,
        endpoint=None,
        ticker=None,
        fromdate=None,
        todate=None,
        tradedate=None,
        dte=None,
        delta=None,
        fields=None,
        strike=None,
        symbols=None,
        expirdate=None,
    ) -> pl.DataFrame | None:
        # Setup Messaging ----
        m = msg.log_message
        # REQUIRED PARAMETERS ----
        address: str = ORATS_BASE_URL
        address += f"{ORATS_ENDPOINTS[endpoint]}"
        address += f"?token={self.token}&ticker={ticker}"

        # OPTIONAL PARAMETERS ----
        if fields is not None:
            address += f"&fields={','.join(fields)}"
        if dte is not None:
            address += f"&dte={','.join(map(str, dte))}"
        if delta is not None:
            address += f"&delta={','.join(map(str, delta))}"
        if tradedate is not None:
            address += f"&tradeDate={tradedate}"
        if strike is not None:
            address += f"&strike={strike}"
        if symbols is not None:
            address += f"&symbols={','.join(map(str, symbols))}"
        if expirdate is not None:
            address += f"&expirDate={expirdate}"

        # Query ORATS API
        r = requests.get(address, timeout=10)

        if r.status_code != 200:
            m(
                msg=f"[orange1]ORATS[/orange1] request "
                f"[bright_red]failed[/bright_red]: "
                f"[steel_blue1]{address}[/steel_blue1]"
                f"\n[bmagenta]Status: {r.status_code}[/bmagenta] "
                f"\n[bmagenta]Message: {r.text}[/bmagenta]",
                status="error",
                silent=self.silent,
            )
            return None

        # Convert to DataFrame

        try:
            data = pl.DataFrame(json.loads(r.text)["data"])
        except Exception as e1:
            try:
                data = json.loads(r.text)["data"]
                data = pl.DataFrame(
                    data, infer_schema_length=round(len(data) / 2)
                )
            except Exception as e2:
                new_error = RuntimeError(
                    f"Both API response conversions failed. First error: {e1}.\nSecond error: {e2}."  # noqa: E501
                )
                raise new_error from e2

        # Subset the data if fromdate and todate are not None
        if fromdate is not None and todate is not None:
            assert fromdate >= date(
                2007, 1, 3
            ), "`fromdate` must be after '2007-01-03'"
            assert (
                todate <= date.today()
            ), "`todate` must not be after today's date"
            assert fromdate < todate, "`fromdate` must be earlier than `todate`"
            data = data.filter(
                (pl.col("tradeDate") >= str(fromdate))
                & (pl.col("tradeDate") <= str(todate))
            )
        return data

    def _get_data_ivol(
        self,
        endpoint=None,
        ticker=None,
        fromdate=None,
        todate=None,
        tradedate=None,
        dte=None,
        delta=None,
        fields=None,
    ) -> pl.DataFrame | None:
        # Setup Messaging ----
        m = msg.log_message

        # REQUIRED PARAMETERS ----
        address: str = ORATS_BASE_URL
        address += f"{ORATS_ENDPOINTS[endpoint]}"
        address += f"?token={self.token}&ticker={ticker}"

        # OPTIONAL PARAMETERS ----
        # Set default fields
        if fields is None:
            if endpoint == "strikesHistory":
                fields = [
                    "ticker",
                    "tradeDate",
                    "expirDate",
                    "dte",
                    "stockPrice",
                    "putBidIv",
                    "putAskIv",
                    "putMidIv",
                    "callMidIv",
                    "callBidIv",
                    "callAskIv",
                ]
            elif endpoint == "ivRankHistory":
                fields = None
            elif endpoint == "summariesHistory":
                fields = [
                    "ticker",
                    "tradeDate",
                    "stockPrice",
                    "exErnIv30d",
                    "iv30d",
                    "fwd60_30",
                ]
            elif endpoint == "coreDataHistory":
                fields = [
                    "ticker",
                    "tradeDate",
                    "atmIvM1",
                    "atmIvM2",
                    "atmIvM3",
                    "atmIvM4",
                    "iv30d",
                ]

        if fields is not None:
            address += f"&fields={','.join(fields)}"
        if dte is not None:
            address += f"&dte={','.join(map(str, dte))}"
        if delta is not None:
            address += f"&delta={','.join(map(str, delta))}"
        if tradedate is not None:
            address += f"&tradeDate={tradedate}"

        # Query ORATS API
        r = requests.get(address, timeout=10)

        if r.status_code != 200:
            m(
                msg=f"[orange1]ORATS[/orange1] request "
                f"[bright_red]failed[/bright_red]: "
                f"[steel_blue1]{address}[/steel_blue1]"
                f"\n[bmagenta]Status: {r.status_code}[/bmagenta] "
                f"\n[bmagenta]Message: {r.text}[/bmagenta]",
                status="error",
                silent=self.silent,
            )
            return None

        # Convert to DataFrame

        try:
            data = pl.DataFrame(json.loads(r.text)["data"])
        except Exception as e1:
            try:
                data = json.loads(r.text)["data"]
                data = pl.DataFrame(
                    data, infer_schema_length=round(len(data) / 2)
                )
            except Exception as e2:
                new_error = RuntimeError(
                    f"Both API response conversions failed. First error: {e1}.\nSecond error: {e2}."  # noqa: E501
                )
                raise new_error from e2

        # Subset the data if fromdate and todate are not None
        if fromdate is not None and todate is not None:
            assert fromdate >= date(
                2007, 1, 3
            ), "`fromdate` must be after '2007-01-03'"

            assert (
                todate <= date.today()
            ), "`todate` must not be after today's date"

            assert fromdate < todate, "`fromdate` must be earlier than `todate`"
            data = data.filter(
                (pl.col("tradeDate") >= str(fromdate))
                & (pl.col("tradeDate") <= str(todate))
            )

        return data
