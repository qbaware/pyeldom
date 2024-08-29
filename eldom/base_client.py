import json
import aiohttp


class BaseClient:
    """
    Eldom Base API client.

    It offers basic API calls like login, logout, get user data, get available devices, etc.

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
        :param session: An optional session object.
        """

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
        return json.loads(await response.text())

    async def get_devices(self):
        """
        Get the devices information.

        :return: The devices information.
        """
        devices_url = f"{self.base_url}/api/device/getmy"
        response = await self.session.get(devices_url)
        response.raise_for_status()
        return json.loads(await response.text())

    async def get_device(self, device_id):
        """
        Get the device information.

        :param device_id: The device ID.
        :return: The device information.
        """
        url = f"{self.base_url}/api/device/getmydevice"
        payload = {"deviceId": device_id}
        response = await self.session.post(url, json=payload)
        response.raise_for_status()
        return json.loads(await response.text())
