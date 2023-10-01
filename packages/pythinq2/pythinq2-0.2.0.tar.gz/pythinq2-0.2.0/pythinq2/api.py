import hashlib
import logging
import time

import requests

from pythinq2.gateway import Gateway
from pythinq2.auth import ThinqAuth
from pythinq2.utils import random_string
from pythinq2.constants import API_KEY, CLIENT_ID

LOGGER = logging.getLogger(__name__)


class ThinqAPI:
    def __init__(
        self, username=None, password=None, language="en-US", country_code="US"
    ):
        """Create a new API object."""
        self.username = username
        self.password = password
        self.language = language
        self.country_code = country_code

        self._gateway = None
        self._auth = None
        self._client_id = None

        self._session = requests.Session()

    @property
    def client_id(self):
        if self._client_id:
            return self._client_id

        if self._auth and self._auth.is_authenticated:
            timestamp = int(time.time() * 1000)
            self._client_id = hashlib.sha256(
                f"{self._auth.user_no}{timestamp}".encode("utf-8"),
            ).hexdigest()
            return self._client_id

        return CLIENT_ID

    def _request(self, method, uri, data=None):
        # Ensure user is authenticated
        self.authenticate()

        headers = {
            "x-api-key": API_KEY,
            "x-thinq-app-ver": "3.6.1200",
            "x-thinq-app-type": "NUTS",
            "x-thinq-app-level": "PRD",
            "x-thinq-app-os": "ANDROID",
            "x-thinq-app-logintype": "LGE",
            "x-service-code": "SVC202",
            "x-country-code": self._auth._gateway.country_code,
            "x-language-code": self._auth._gateway.language_code,
            "x-service-phase": "OP",
            "x-origin": "app-native",
            "x-model-name": "samsung/SM-G930L",
            "x-os-version": "AOS/7.1.2",
            "x-app-version": "LG ThinQ/3.6.12110",
            "x-message-id": random_string(22),
            "user-agent": "okhttp/3.14.9",
            "x-client-id": self.client_id,
        }

        if self._auth and self._auth.is_authenticated:
            headers["x-emp-token"] = self._auth._access_token
            headers["x-user-no"] = self._auth.user_no

        req = requests.Request(
            method=method,
            url=f"{self._auth._gateway.thinq2_api}{uri}",
            json=data,
            headers=headers,
        )
        response = self._session.send(req.prepare())
        response.raise_for_status()
        return response.json()

    def authenticate(self):
        """Authenticate an user on LG API."""
        if self._auth and self._auth.is_authenticated:
            return

        self._auth = ThinqAuth(
            gateway=Gateway(
                country_code=self.country_code,
                language=self.language,
            ),
        )
        return self._auth.login(self.username, self.password)

    def get_homes(self):
        return self._request(method="GET", uri="/service/homes")["result"][
            "item"
        ]

    def get_home(self, home_id):
        return self._request(method="GET", uri=f"/service/homes/{home_id}")

    def send_command(self, device_id, data):
        return self._request(
            method="POST",
            uri=f"/service/devices/{device_id}/control-sync",
            data={
                "ctrlKey": "basicCtrl",
                "command": "Set",
                **data,
            },
        )
