"""A CLI tool to control your LG devices.

Usage:
  pythinq2 authenticate <username> <password> [--country <country>] [--language <language>]
  pythinq2 get-homes <username> <password> [--country <country>] [--language <language>]
  pythinq2 get-home <username> <password> <home_id> [--country <country>] [--language <language>]
"""  # noqa: E501
import datetime
import logging

from docopt import docopt
from tabulate import tabulate

from pythinq2 import __version__, ThinqAPI

LOGGER = logging.getLogger(__name__)


def authenticate(username, password, country="US", language="en-US"):
    """Authenticate user and get token from LG API."""
    LOGGER.info("Authentication as: %s", username)

    api = ThinqAPI(
        username=username,
        password=password,
        country_code=country,
        language=language,
    )
    token = api.authenticate()
    now = datetime.datetime.now()

    print(
        tabulate(
            [
                ["Access Token", token["access_token"]],
                ["Refresh Token", token["refresh_token"]],
                ["Oauth2 Backend URL", token["oauth2_backend_url"]],
                [
                    "Expires at",
                    now + datetime.timedelta(seconds=int(token["expires_in"])),
                ],
            ],
            tablefmt="fancy_grid",
        ),
    )


def get_homes(username, password, country="US", language="en-US"):
    api = ThinqAPI(
        username=username,
        password=password,
        country_code=country,
        language=language,
    )
    data = []

    for home in api.get_homes():
        data.append([home["homeId"], home["homeName"]])

    print(tabulate(data, headers=["#", "Name"], tablefmt="fancy_grid"))


def get_home(username, password, home_id, country="US", language="en-US"):
    api = ThinqAPI(
        username=username,
        password=password,
        country_code=country,
        language=language,
    )

    print(api.get_home(home_id))


def main():
    """Entry point."""
    args = docopt(__doc__, version=__version__)

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    if args["authenticate"]:
        authenticate(
            username=args["<username>"],
            password=args["<password>"],
            country=args["<country>"],
            language=args["<language>"],
        )
    if args["get-homes"]:
        get_homes(
            username=args["<username>"],
            password=args["<password>"],
            country=args["<country>"],
            language=args["<language>"],
        )
    if args["get-home"]:
        get_home(
            username=args["<username>"],
            password=args["<password>"],
            home_id=args["<home_id>"],
            country=args["<country>"],
            language=args["<language>"],
        )


if __name__ == "__main__":
    main()
