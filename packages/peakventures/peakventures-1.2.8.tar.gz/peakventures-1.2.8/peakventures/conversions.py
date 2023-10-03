import datetime
import json
import logging
from typing import Optional

import requests
from websockets.sync import client as websocket

DEV_URL = "wss://dev.adtechapi.xyz/conversions/stream"
LIVE_URL = "wss://live.adtechapi.xyz/conversions/stream"

AUTH_URL = "https://peakventures.us.auth0.com/oauth/token"
AUTH_AUDIENCE = "https://api.peakventures.co"
AUTH_GRANT_TYPE = "client_credentials"

logger_handler = logging.StreamHandler()
logger_handler.setLevel(logging.INFO)
logger_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logger_handler)


class ConversionsClient:
    client_id: str
    client_secret: str

    url: str

    initialized: bool = False

    connection: websocket.Connection
    conversions_number = 0

    _access_token: str = None

    @property
    def access_token(self: "ConversionsClient") -> str:
        """Return access token."""
        if not self._access_token:
            self._access_token = self.__get_access_token()

        return self._access_token

    def __init__(
            self: "ConversionsClient",
            client_id: str,
            client_secret: str,
            url: str = LIVE_URL,
            access_token: Optional[str] = None) -> None:
        """
        Initialize Conversions Client.

        :param client_id: Auth0 client id.
        :param client_secret: Auth0 client secret.
        :param url: WebSocket API URL.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.url = url
        self._access_token = access_token

    def __enter__(self: "ConversionsClient") -> "ConversionsClient":
        """Enter context manager."""
        self.connection = websocket.connect(self.url, additional_headers={
            "Authorization": f"Bearer {self.access_token}"
        })

        self.initialized = True

        logger.info("Connected to %s", self.url)

        return self

    def __exit__(self: "ConversionsClient", exc_type, exc_val, exc_tb) -> None:
        """Exit context manager."""
        logger.info("Streamed %d conversions", self.conversions_number)

        self.connection.close()

        logger.info("Disconnected from %s", self.url)

        self.initialized = False

    def send(
            self: "ConversionsClient",
            buyside_network: str,
            buyside_network_account: str,
            partner_id: str,
            pixel_id: str,
            pixel_event: str,
            click_id: str,
            conversion_date: int | datetime.datetime,
            user_agent: str,
            ip_address: str,
            conversion_value: float,
            skip_deduplication: bool = False) -> None:
        """
        Send conversion event.

        :param buyside_network: Buyside network name.
        :param buyside_network_account: Buyside network account name.
        :param partner_id: Partner id.
        :param pixel_id: Pixel id.
        :param pixel_event: Pixel event.
        :param click_id: Click id.
        :param conversion_date: Conversion date.
        :param user_agent: User agent.
        :param ip_address: IP address.
        :param conversion_value: Conversion value.
        :param skip_deduplication: Skip deduplication.
        """
        if isinstance(conversion_date, datetime.datetime):
            conversion_date_unix_timestamp = int(conversion_date.timestamp())
        else:
            conversion_date_unix_timestamp = conversion_date

        if not self.initialized:
            raise RuntimeError("ConversionsClient is not initialized, use `with` statement")

        self.connection.send(json.dumps({
            "BuysideNetwork": buyside_network,
            "BuysideNetworkAccount": buyside_network_account,
            "PartnerId": partner_id,
            "PixelId": pixel_id,
            "PixelEvent": pixel_event,
            "ClickId": click_id,
            "ConversionDate": conversion_date_unix_timestamp,
            "UserAgent": user_agent,
            "IpAddress": ip_address,
            "ConversionValue": conversion_value,
            "SkipDeduplication": skip_deduplication
        }))

        self.conversions_number += 1

    def __get_access_token(self: "ConversionsClient") -> str:
        """Get JWT token from client credentials."""
        auth_response = requests.post(
            AUTH_URL,
            json={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "audience": AUTH_AUDIENCE,
                "grant_type": AUTH_GRANT_TYPE
            },
        )

        auth_response.raise_for_status()

        auth_response_json = auth_response.json()

        logger.info("Got access token %s", auth_response_json["access_token"])

        return auth_response_json["access_token"]
