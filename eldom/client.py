import json
import aiohttp

from .convector_heater import ConvectorHeaterClient
from .constants import BASE_URL
from .flat_boiler import FlatBoilerClient
from .models import Device, Language, User
from .smart_boiler import SmartBoilerClient


class Client:
    """
    Eldom main API client for the `myeldom.com` APIs.

    It offers basic API calls like login, logout, get user data, get available devices, etc.

    It also offers access to the flat boiler and smart boiler clients.

    Before using the client, you need to login with the login method.
    """

    def __init__(
        self,
        session: aiohttp.ClientSession,
    ):
        """
        Initialize the Eldom API client.

        Make sure to login with the login method before using the other methods of the client.

        :param session: A session object.
        """
        self.session = session

        self.flat_boiler = FlatBoilerClient(session)
        self.smart_boiler = SmartBoilerClient(session)
        self.convector_heater = ConvectorHeaterClient(session)

    async def close(self):
        """
        Close the session.
        """
        await self.session.close()

    async def login(self, email, password):
        """
        Perform login and store the authentication cookie in the session.

        :param email: The email for login.
        :param password: The password for login.
        """
        login_url = f"{BASE_URL}/Account/Login"
        payload = {"Email": email, "Password": password}
        response = await self.session.post(login_url, data=payload)
        response.raise_for_status()

    async def logout(self):
        """
        Perform logout and clear the authentication cookie from the session.
        """
        logout_url = f"{BASE_URL}/account/logout"
        response = await self.session.get(logout_url)
        response.raise_for_status()
        self.session.cookie_jar.clear()

    async def get_user(self):
        """
        Get the user information.

        :return: The user information.
        """
        user_url = f"{BASE_URL}/api/user/get"
        response = await self.session.get(user_url)
        response.raise_for_status()
        response_json = json.loads(await response.text())
        response_json["language"] = Language(response_json["language"])
        response_json["lastLoginDate"] = response_json["lastLoginDate"]
        response_json["lastActiveDate"] = response_json["lastActiveDate"]
        return User(**response_json)

    async def get_devices(self):
        """
        Get the devices information.

        :return: The devices information.
        """
        devices_url = f"{BASE_URL}/api/device/getmy"
        response = await self.session.get(devices_url)
        response.raise_for_status()
        response_json = json.loads(await response.text())
        devices = []
        for device_json in response_json:
            device_json["lastDataRefreshDate"] = device_json["lastDataRefreshDate"]
            devices.append(Device(**device_json))
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
