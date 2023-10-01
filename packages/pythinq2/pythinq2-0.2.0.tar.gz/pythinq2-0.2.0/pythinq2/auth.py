from email.utils import format_datetime
import hashlib
from urllib.parse import quote, urlencode, urlparse, parse_qs, unquote
import datetime
import logging

import requests

from pythinq2.constants import (
    APPLICATION_KEY,
    OAUTH_CLIENT_KEY,
    OAUTH_SECRET_KEY,
    CLIENT_ID,
)
from pythinq2.utils import generate_signature

LOGGER = logging.getLogger(__name__)


class ThinqAuth:
    def __init__(self, gateway):
        """Create a ThinqAuth object."""
        self._gateway = gateway

        self._access_token = None
        self._refresh_token = None
        self._oauth2_backend_url = None
        self._user_no = None

    @property
    def is_authenticated(self):
        return bool(self._access_token)

    @property
    def user_no(self):
        if self._user_no:
            return self._user_no

        timestamp = format_datetime(datetime.datetime.utcnow())
        profile_url = f"{self._oauth2_backend_url}users/profile"
        signature = generate_signature(
            f"/users/profile\n{timestamp}",
            OAUTH_SECRET_KEY,
        )

        response = requests.get(
            url=profile_url,
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {self._access_token}",
                "X-Lge-Svccode": "SVC202",
                "X-Application-Key": APPLICATION_KEY,
                "lgemp-x-app-key": CLIENT_ID,
                "X-Device-Type": "M01",
                "X-Device-Platform": "ADR",
                "x-lge-oauth-date": timestamp,
                "x-lge-oauth-signature": signature,
            },
        )
        response.raise_for_status()

        body = response.json()

        # The access token might need to be refreshed
        if body.get("lgoauth_error_code") == "LG.OAUTH.EC.2004":
            LOGGER.debug("LG API access token has expired, refreshing it")
            self.refresh_token()
            return self.user_no

        self._user_no = response.json()["account"]["userNo"]
        return self._user_no

    def login(self, username, password):
        """Log the user on the Thinq API."""
        encrypted_password = hashlib.sha512(
            password.encode("utf-8")
        ).hexdigest()
        headers = {
            "Accept": "application/json",
            "X-Application-Key": APPLICATION_KEY,
            "X-Client-App-Key": OAUTH_CLIENT_KEY,
            "X-Lge-Svccode": "SVC709",
            "X-Device-Type": "M01",
            "X-Device-Platform": "ADR",
            "X-Device-Language-Type": "IETF",
            "X-Device-Publish-Flag": "Y",
            "X-Device-Country": self._gateway.country_code,
            "X-Device-Language": self._gateway.language_code,
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Access-Control-Allow-Origin": "*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
        }

        response = requests.post(
            url=f"{self._gateway.login_base_url}/preLogin",
            params={
                "user_auth2": encrypted_password,
                "log_param": (
                    f"login request / user_id: {username} / third_party: "
                    "null / svc_list : SVC202,SVC710 / 3rd_service : "
                ),
            },
            headers=headers,
        )
        response.raise_for_status()

        pre_login = response.json()
        headers["X-Signature"] = pre_login["signature"]
        headers["X-Timestamp"] = pre_login["tStamp"]

        response = requests.post(
            url=(
                f"{self._gateway.emp_base_url}/emp/v2.0/account/session"
                f"/{quote(username)}"
            ),
            params={
                "user_auth2": pre_login["encrypted_pw"],
                "password_hash_prameter_flag": "Y",
                "svc_list": "SVC202,SVC710",
            },
            headers=headers,
        )
        response.raise_for_status()

        account = response.json()["account"]
        response = requests.get(
            url=f"{self._gateway.login_base_url}/searchKey",
            params={
                "key_name": "OAUTH_SECRETKEY",
                "sever_type": "OP",
            },
            headers=headers,
        )
        response.raise_for_status()

        secret_key = response.json()["returnData"]
        timestamp = format_datetime(datetime.datetime.utcnow())
        emp_data = {
            "account_type": account["userIDType"],
            "client_id": "LGAO221A02",
            "country_code": account["country"],
            "redirect_uri": "lgaccount.lgsmartthinq:/",
            "response_type": "code",
            "state": "12345",
            "username": account["userID"],
        }
        emp_url = (
            "https://emp-oauth.lgecloud.com/emp/oauth2/authorize/"
            f"empsession?{urlencode(emp_data)}"
        )
        parsed = urlparse(emp_url)
        signature = generate_signature(
            f"{parsed.path}?{parsed.query}\n{timestamp}",
            secret_key,
        )

        response = requests.get(
            url=emp_url,
            headers={
                "lgemp-x-app-key": OAUTH_CLIENT_KEY,
                "lgemp-x-date": timestamp,
                "lgemp-x-session-key": account["loginSessionID"],
                "lgemp-x-signature": signature,
                "Accept": "application/json",
                "X-Device-Type": "M01",
                "X-Device-Platform": "ADR",
                "Content-Type": "application/x-www-form-urlencoded",
                "Access-Control-Allow-Origin": "*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.44"
                ),
            },
        )
        response.raise_for_status()

        redirect_uri = response.json()["redirect_uri"]
        parsed = urlparse(redirect_uri)
        qs = parse_qs(parsed.query)

        token_data = {
            "code": qs["code"][0],
            "grant_type": "authorization_code",
            "redirect_uri": emp_data["redirect_uri"],
        }
        response = requests.post(
            url=f"{qs['oauth2_backend_url'][0]}oauth/1.0/oauth2/token",
            params=token_data,
            headers={
                "x-lge-app-os": "ADR",
                "x-lge-appkey": CLIENT_ID,
                "x-lge-oauth-signature": generate_signature(
                    (
                        f"/oauth/1.0/oauth2/token?{urlencode(token_data)}"
                        f"\n{timestamp}"
                    ),
                    OAUTH_SECRET_KEY,
                ),
                "x-lge-oauth-date": timestamp,
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        response.raise_for_status()

        token = response.json()
        token["oauth2_backend_url"] = unquote(token["oauth2_backend_url"])

        self._access_token = token["access_token"]
        self._refresh_token = token["refresh_token"]
        self._oauth2_backend_url = token["oauth2_backend_url"]
        return token

    def refresh_token(self):
        """Refresh access token."""
        token_url = f"{self._oauth2_backend_url}oauth/1.0/oauth2/token"
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self._refresh_token,
        }
        timestamp = format_datetime(datetime.datetime.utcnow())

        request_url = f"/oauth/1.0/oauth2/token?{urlencode(data)}"
        signature = generate_signature(
            f"{request_url}\n{timestamp}", OAUTH_SECRET_KEY
        )

        response = requests.post(
            url=token_url,
            params=data,
            headers={
                "x-lge-app-os": "ADR",
                "x-lge-appkey": CLIENT_ID,
                "x-lge-oauth-signature": signature,
                "x-lge-oauth-date": timestamp,
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        response.raise_for_status()

        self._access_token = response.json()["access_token"]
