import json
import aiohttp

from .convector_heater import ConvectorHeaterClient
from .constants import BASE_URL
from .flat_boiler import FlatBoilerClient
from .models import Device, User
from .token_provider import TokenProvider


class Client:
    """
    Eldom main API client for the `iot.myeldom.com` APIs.

    It offers basic API calls like login, logout, get user data, get available devices, etc.

    It also offers access to a convector heater client.

    Before using the client, you need to login with the login method.
    """

    def __init__(
        self,
        session: aiohttp.ClientSession,
        username: str,
        password: str,
    ):
        """
        Initialize the Eldom API client.

        Make sure to login with the login method before using the other methods of the client.

        :param session: A session object.
        """
        self.session = session
        self.token_provider = TokenProvider(session, username, password)

        self.convector_heater = ConvectorHeaterClient(session, self.token_provider)
        self.flat_boiler = FlatBoilerClient(session, self.token_provider)

    async def close(self):
        """
        Close the session.
        """
        await self.session.close()

    async def get_user(self):
        """
        Get the user information.

        :return: The user information.
        """

        user_url = f"{BASE_URL}/api/account"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0",
            "Authorization": f"Bearer {await self.token_provider.provide()}",
        }
        response = await self.session.get(user_url, headers=headers)
        response.raise_for_status()
        response_json = json.loads(await response.text())

        supported_fields = {field.name for field in User.__dataclass_fields__.values()}
        filtered_user_json = {
            k: v for k, v in response_json.items() if k in supported_fields
        }

        return User(**filtered_user_json)

    async def get_devices(self):
        """
        Get the devices information.

        :return: The devices information.
        """

        devices_url = f"{BASE_URL}/api/device-list?page=1&size=1000"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0",
            "Authorization": f"Bearer {await self.token_provider.provide()}",
            "Content-Type": "application/json",
            "ionic-idd": "0",
        }
        response = await self.session.get(devices_url, headers=headers)
        response.raise_for_status()
        response_json = json.loads(await response.text())
        devices = []
        for device_json in response_json:
            supported_fields = {
                field.name for field in Device.__dataclass_fields__.values()
            }
            filtered_json = {
                k: v for k, v in device_json.items() if k in supported_fields
            }

            devices.append(Device(**filtered_json))
        return devices

    async def is_connected(self):
        """
        Check whether the connection is established.

        :return: Boolean showing if the client is connected.
        """
        try:
            await self.get_devices()
            return True
        except Exception:
            return False
