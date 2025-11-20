import jwt
import aiohttp
from datetime import datetime

from .constants import BASE_URL

def is_token_expired(token):
    """
    Check if a JWT token is expired.

    :param token: The JWT token string
    :return: True if expired, False if still valid
    """
    try:
        payload = jwt.decode(jwt=token, options={"verify_signature": False})

        exp_timestamp = payload.get("exp")
        if not exp_timestamp:
            return True

        exp_datetime = datetime.fromtimestamp(exp_timestamp)
        return datetime.now() >= exp_datetime

    except jwt.InvalidTokenError:
        return True


class TokenProvider:
    """
    A simple token provider.
    """

    def __init__(
        self,
        session: aiohttp.ClientSession,
        username: str,
        password: str,
    ):
        self.session = session
        self.username = username
        self.password = password

        self.token = None

    async def provide(self):
        """
        Provide a valid token.

        :return: The token string.
        """
        if self.token is None or is_token_expired(self.token):
            login_url = f"{BASE_URL}/api/authenticate"
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:133.0) Gecko/20100101 Firefox/133.0",
                "Content-Type": "application/json",
            }
            payload = {"username": self.username, "password": self.password, "rememberMe": False}
            response = await self.session.post(login_url, json=payload, headers=headers)
            response.raise_for_status()

            response_json = await response.json()
            self.token = response_json.get("id_token")

            if not self.token:
                raise ValueError("No access token received from login response")
        
        return self.token
