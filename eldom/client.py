import json
import aiohttp

from .flat_boiler import FlatBoilerClient
from .models import Device, Language, User
from .smart_boiler import SmartBoilerClient


class Client(FlatBoilerClient, SmartBoilerClient):
    """
    Eldom main API client.

    It offers basic API calls like login, logout, get user data, get available devices, etc.

    It also offers access to the flat boiler and smart boiler clients.

    Before using the client, you need to login with the login method.
    """

    def __init__(
        self,
        base_url: str,
        session: aiohttp.ClientSession,
    ):
        """
        Initialize the Eldom API client.

        Make sure to login with the login method before using the other methods of the client.

        :param base_url: The base URL for the API.
        :param session: A session object.
        """
        FlatBoilerClient.__init__(self, base_url=base_url, session=session)
        SmartBoilerClient.__init__(self, base_url=base_url, session=session)

        self.base_url = base_url
        self.session = session

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
        login_url = f"{self.base_url}/Account/Login"
        payload = {"Email": email, "Password": password}
        response = await self.session.post(login_url, data=payload)
        response.raise_for_status()

    async def logout(self):
        """
        Perform logout and clear the authentication cookie from the session.
        """
        logout_url = f"{self.base_url}/account/logout"
        response = await self.session.get(logout_url)
        response.raise_for_status()
        self.session.cookies.clear()
        await self.session.cookie_jar.clear()

    async def get_user(self):
        """
        Get the user information.

        :return: The user information.
        """
        user_url = f"{self.base_url}/api/user/get"
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
        devices_url = f"{self.base_url}/api/device/getmy"
        response = await self.session.get(devices_url)
        response.raise_for_status()
        response_json = json.loads(await response.text())
        devices = []
        for device_json in response_json:
            device_json["lastDataRefreshDate"] = device_json["lastDataRefreshDate"]
            devices.append(Device(**device_json))
        return devices
