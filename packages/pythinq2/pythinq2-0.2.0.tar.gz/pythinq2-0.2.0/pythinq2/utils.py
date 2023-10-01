import base64
import hashlib
import hmac
import random
import string


def random_string(n):
    """Generate a random string of `n` characters."""
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=n))


def generate_signature(message, secret):
    """Encode a message with a secret key."""
    return base64.b64encode(
        hmac.new(
            secret.encode("utf-8"),
            message.encode("utf-8"),
            hashlib.sha1,
        ).digest(),
    ).decode("utf-8")
