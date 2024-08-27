import requests


class Client:
    """
    Eldom API client.

    Before using the client, you need to login with the login method.
    """

    def __init__(self, base_url, timeout=30):
        """
        Initialize the Eldom API client.

        Make sure to login with the login method before using the other methods of the client.

        :param base_url: The base URL for the API.
        :param api_key: The API key for authentication (if required).
        :param timeout: Timeout for API requests.
        """

        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()

    def login(self, email, password):
        """
        Perform login and store the authentication cookie in the session.

        :param email: The email for login.
        :param password: The password for login.
        """
        login_url = f"{self.base_url}/Account/Login"
        payload = {"Email": email, "Password": password}
        response = self.session.post(login_url, data=payload, timeout=self.timeout)
        response.raise_for_status()

    def logout(self):
        """
        Perform logout and clear the authentication cookie from the session.
        """
        logout_url = f"{self.base_url}/account/logout"
        response = self.session.get(logout_url, timeout=self.timeout)
        response.raise_for_status()
        self.session.cookies.clear()

    def get_user(self):
        """
        Get the user information.

        :return: The user information.
        """
        user_url = f"{self.base_url}/api/user/get"
        response = self.session.get(user_url, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_devices(self):
        """
        Get the devices information.

        :return: The devices information.
        """
        devices_url = f"{self.base_url}/api/device/getmy"
        response = self.session.get(devices_url, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_device(self, device_id):
        """
        Get the device information.

        :param device_id: The device ID.
        :return: The device information.
        """
        url = f"{self.base_url}/api/device/getmydevice"
        payload = {"deviceId": device_id}
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def set_flat_boiler_state(self, device_id, state):
        """
        Set the state of a flat boiler device.

        :param device_id: The device ID.
        :param state: The state to set (e.g., 0 to turn off, 1 to turn on heating, 2 to turn on Smart mode, 3 to turn on Study mode).
        :return: The response from the server.
        """
        url = f"{self.base_url}/api/flatboiler/setState"
        payload = {"deviceId": device_id, "state": state}
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
