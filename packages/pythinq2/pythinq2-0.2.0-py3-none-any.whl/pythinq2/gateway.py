import logging

import requests

from pythinq2.utils import random_string
from pythinq2.constants import (
    GATEWAY_URL,
    API_KEY,
    SERVICE_CODE,
    API_CLIENT_ID,
)

LOGGER = logging.getLogger(__name__)


class Gateway:
    def __init__(self, country_code, language, load=True):
        """Create a new Gateway object."""
        self._session = requests.Session()
        self._session.headers = {
            "x-api-key": API_KEY,
            "x-thinq-app-ver": "3.6.1200",
            "x-thinq-app-type": "NUTS",
            "x-thinq-app-level": "PRD",
            "x-thinq-app-os": "ANDROID",
            "x-thinq-app-logintype": "LGE",
            "x-service-code": SERVICE_CODE,
            "x-country-code": country_code,
            "x-language-code": language,
            "x-service-phase": "OP",
            "x-origin": "app-native",
            "x-model-name": "samsung/SM-G930L",
            "x-os-version": "AOS/7.1.2",
            "x-app-version": "LG ThinQ/3.6.12110",
            "x-message-id": random_string(22),
            "user-agent": "okhttp/3.14.9",
            "x-client-id": API_CLIENT_ID,
        }

        self._data = None

        if load:
            self.load()

    @property
    def login_base_url(self):
        return self._data["empSpxUri"]

    @property
    def country_code(self):
        return self._data["countryCode"]

    @property
    def language_code(self):
        return self._data["languageCode"]

    @property
    def emp_base_url(self):
        return self._data["empTermsUri"]

    @property
    def thinq2_api(self):
        return self._data["thinq2Uri"]

    def load(self):
        """Load data from remote gateway."""
        LOGGER.debug("Loading data from gateway: %s", GATEWAY_URL)

        response = self._session.get(GATEWAY_URL)
        response.raise_for_status()
        self._data = response.json()["result"]
