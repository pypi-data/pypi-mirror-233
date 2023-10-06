try:
    import ujson as json # type: ignore # noqa
except ImportError:
    import json
import logging
import threading
import time
from typing import Union

import requests
from .models import ClientList, DonateList, LongpoolDonate, User
from .events import Event

logging.basicConfig(
    format="[%(asctime)s] %(levelname)s: %(message)s", level=logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)

API_VERSION = "v1"


class Donatello:

    def __init__(self,
                 token: str,
                 widget_id: str = None,
                 longpool_timeout: int = 1,
                 logging_level: int = logging.INFO
        ) -> None:
        """Donatello API wrapper

            :param token: Donatello API token
            :param widget_id: Donatello widget ID
            :param longpool_timeout: Long polling timeout
            :param logging_level: Logging level

            :type token: str
            :type widget_id: str
            :type longpool_timeout: int
            :type logging_level: int

            :return: Donatello API wrapper
            :rtype: Donatello

            :raises Exception: If API returns error

            Basic Usage::

                >>> from donatello.client import Donatello
                >>> from donatello.models import LongpoolDonate, User
                >>> client = Donatello("your_token", "widget_id")

                >>> print(client.get_me()) # Get user info
                >>> print(client.get_donates()) # Get donates
                >>> print(client.get_clients()) # Get clients

                >>> @client.on_client # On client event
                >>> def on_client(client: User):
                >>>     print(f"Client name: {client.nickname}")
                >>>     print(f"Total donates: {client.donates.total_amount}")

                >>> @client.on_donate # On donate event
                >>> def on_donate(donate: LongpoolDonate):
                >>>     print("------- NEW DONATE -------")
                >>>     print(f"Nickname: {donate.name}")
                >>>     print(f"Amount: {donate.amount} {donate.currency}")
                >>>     print(f"Message: {donate.message}")
                >>>     print(f"Date: {donate.created_at}")
                >>>     print(f"Client name: {donate.client_name}")
                >>> client.start() # Start long polling

        """

        # Logging
        self._logger = logging.getLogger("donatello")
        self._logger.setLevel(logging_level)

        # URLs
        self._api_url = f"https://donatello.to/api/{API_VERSION}/"
        self._widget_url = f"https://donatello.to/widget/{widget_id}/token/{token}/"
        self._session = requests.Session()

        # Events
        self.__on_error = Event()
        self.__on_client = Event()
        self.__on_donate = Event()

        self.on_donate = self.__on_donate.on_donate
        self.on_client = self.__on_client.on_client
        self.on_error = self.__on_error.on_error

        # Long polling
        if not widget_id:
            self._logger.warning(
                "Widget ID is not specified. You can't use long polling.")
            self._is_long_polling = False
        else:
            self._is_long_polling = True
            self._longpool_timeout = longpool_timeout
        self._stop_long_polling = False

        # Token
        self._token = token
        self._headers = {
            "X-Token": self._token,
        }
        self._session.headers.update(self._headers)

    def _request(self,
                 method: str,
                 url: str,
                 endpoint: str,
                 **kwargs
        ) -> dict:
        """Make a request to API
            Returns :class: `dict` with response

            :param method: HTTP method
            :param url: API url
            :param endpoint: API endpoint
            :param **kwargs: Additional arguments for requests.request
        """
        resp = self._session.request(
            method, url + endpoint, **kwargs)
        data: dict = json.loads(resp.text)
        self._logger.debug(f"Response: {data}")
        if data.get("success") is False:
            self._error_handler(data)
        return data

    def _error_handler(self, message: Union[str, dict]) -> None:
        """Handle errors
            :param message: Error message
        """
        self.__on_error.trigger([message])
        self._logger.error(message)

    def get_me(self) -> User:
        """Get user info
            Returns :class: `User` with user info
        """
        return User(**self._request("GET", self._api_url, "me"))

    def get_donates(self, page: int = 0, size: int = 20) -> DonateList:
        """Get donates
            Returns :class: `DonateList` with donates
        """
        return DonateList(**self._request("GET", self._api_url, "donates", params={
            "page": page,
            "size": size
        }))

    def get_clients(self) -> ClientList:
        """Get clients
            Returns :class: `ClientList` with clients
        """
        return ClientList(**self._request("GET", self._api_url, "clients"))

    def _long_polling(self) -> None:
        """Long polling method"""
        self._logger.info("Long polling started.")
        self.__on_client.trigger([self.get_me()])
        while not self._stop_long_polling:
            try:
                resp = self._request("GET", self._widget_url, "info")
                if resp.get("clientName"):
                    self.__on_donate.trigger([LongpoolDonate(**resp)])
                elif not resp.get("success"):
                    self._error_handler(resp)
            except Exception as e:
                self._error_handler(e)
            time.sleep(self._longpool_timeout)

    def start(self) -> None:
        """Start long polling"""
        if self._is_long_polling:
            threading.Thread(target=self._long_polling).start()
        else:
            self._logger.warning(
                "Long polling is disabled. You can't use on_donate, on_error events.")
            self._logger.warning(
                "You can enable long polling by specifying widget ID in constructor.")

    def stop(self) -> None:
        """Stop long polling"""
        self._stop_long_polling = True
        self._logger.info("Long polling stopped.")

    def __del__(self) -> None:
        self.stop()

    def __str__(self) -> str:
        return f"Donatello API wrapper. Widget ID: {self._widget_id}"

    def __repr__(self) -> str:
        return f"Donatello API wrapper. Widget ID: {self._widget_id}"
