import os
import warnings

import requests
from dotenv import load_dotenv, set_key, unset_key

from humbldata.helpers import MessageHelpers


class APICredentials:
    def __init__(self, silent: bool = False):
        self.silent = silent
        self.api_key = None
        # Init Messaging aliases
        self.m = MessageHelpers.log_message
        self.m(
            "Accessing [b steel_blue1]APICredentials[/b steel_blue1] "
            "object!",
            "info",
            silent=self.silent,
        )

    def set_orats(self, api_key: str = None, persist: bool = False):
        """
        This method sets the ORATS API key.

        The API key is stored as an environment variable and optionally
        persisted in a .env file.

        Parameters:
        -----------
        api_key : str, optional
            The API key for ORATS. If not provided, defaults to None.
        persist : bool, optional
            A flag indicating whether to persist the API key in a .env file.
            If True, the API key is written to the .env file. Defaults to False.

        Returns:
        --------
        None

        Example:
        --------
        >>> obj = APICredentials()
        >>> obj.set_orats("YOUR_API_KEY", True)
        """
        self.api_key = api_key
        os.environ["API_ORATS"] = api_key
        self.m(
            "[orange1]ORATS[/orange1] API key set "
            "[green3]successfully[/green3]!",
            "success",
            self.silent,
        )
        if persist:
            set_key(".env", "API_ORATS", api_key)
            self.m(
                "[orange1]ORATS[/orange1] API key persisted in [grey39].env"
                "[/grey39] file!",
                "success",
                self.silent,
            )

    def get_orats(self):
        """
        This method retrieves the ORATS API key from environment variables.

        The method first loads the environment variables from the .env file.
        It then tries to retrieve the value of the "API_ORATS" variable.
        If this variable is not set (i.e., its value is None), an OSError is
        raised with a descriptive message. If the API key is successfully
        retrieved, it is returned by the function.

        Returns:
        --------
        str
            The ORATS API key if it exists in the environment variables.

        Raises:
        ------
        OSError
            If the API key for ORATS doesn't exist in the environment variables.
        """
        load_dotenv(".env")
        try:
            api_key = os.getenv("API_ORATS")
            if api_key is None:
                raise OSError("ORATS API KEY DOES NOT EXIST")
            return api_key
        except OSError:
            self.m(
                "[orange1]ORATS[/orange1] API key does [bright_red]NOT"
                "[/bright_red] exist",
                "error",
                self.silent,
            )
            raise

    def check_orats(self, private_return: bool = False, persist: bool = True):
        """
        This method checks the validity of the ORATS API key.

        The method first retrieves the ORATS API key. It then sends a test
        request to the ORATS API. If the response status code is 200, it means
        the API key is valid. In this case, it sets the api_key attribute and
        optionally updates the "API_ORATS" environment variable with the API
        ey. If the response status code is not 200, it logs an error message
        indicating that the API key failed the test.

        Parameters:
        ----------
        private_return : bool, optional
            If set to True, the method returns the API key. By default, it's set
            to False.
        persist : bool, optional
            If set to True, the method updates the "API_ORATS" environment
            variable with the API key. By default, it's set to True.

        Returns:
        -------
        str or None
            If private_return is set to True, it returns the API key. Otherwise,
            it doesn't return anything.

        Raises:
        ------
        requests.exceptions.RequestException
            If there's any network problem that prevents it from sending the
            request to the ORATS API.
        """
        api_key = self.get_orats()

        self.m(
            "[orange1]ORATS[/orange1] api_key [green3]exists[/green3]",
            "success",
            silent=self.silent,
        )

        # make a test request to the API
        url = f"https://api.orats.io/datav2/tickers?token={api_key}&ticker=AAPL"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            self.m(
                "[orange1]ORATS[/orange1] api_key is " "[green3]valid[/green3]",
                "success",
                silent=self.silent,
            )
            self.api_key = api_key
            if persist:
                os.environ["API_ORATS"] = api_key
            if private_return:
                return self.api_key
        else:
            self.m(
                "[orange1]ORATS[/orange1] api_key was set, failed the test",
                "warning",
            )
            warnings.warn("Invalid ORATS API key!", stacklevel=1)

            return "Invalid Key"

    def remove_orats(self, env: bool = False):
        """
        This method removes the ORATS API key from environment variables and the
        .env file.

        The method first loads the environment variables from the .env file.
        It then tries to remove the "API_ORATS" variable from the environment
        variables.
        If an exception occurs during this process, it is caught and re-raised
        after logging an error message. After that, it attempts to unset the
        "API_ORATS" key in the .env file. Again, if an exception occurs, it is
        caught and re-raised after logging an error message.

        Parameters:
        -----------
        env : bool, optional
            A flag indicating whether to remove the API key from the .env file.

        Raises:
        ------
        Exception
            If there's any issue while removing the API key from environment
            variables or the .env file.
        """
        load_dotenv(".env")
        try:
            os.environ.pop("API_ORATS")
        except Exception as e:
            self.m(str(e), "error")
            raise
        self.m(
            "[orange1]ORATS[/orange1] API key removed from os.environ!",
            "success",
            self.silent,
        )
        if env is True:
            try:
                unset_key(".env", "API_ORATS")
            except Exception as e:
                self.m(str(e), "error")
                raise
            self.m(
                "[orange1]ORATS[/orange1] API key removed!",
                "success",
                self.silent,
            )
