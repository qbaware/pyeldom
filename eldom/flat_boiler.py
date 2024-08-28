from eldom.base_client import _BaseClient


class Client(_BaseClient):
    """
    Eldom API client.

    Before using the client, you need to login with the login method.
    """

    def __init__(self, base_url, timeout=30):
        """
        Initialize the Eldom flat boiler API client.

        Make sure to login with the login method before using the other methods of the client.

        :param base_url: The base URL for the API.
        :param api_key: The API key for authentication (if required).
        :param timeout: Timeout for API requests.
        """

        super().__init__(base_url, timeout)

    def get_flat_boiler_status(self, device_id):
        """
        Get the status of a flat boiler device.

        :param device_id: The device ID.
        :return: The response from the server.
        """
        url = f"{self.base_url}/api/flatboiler/{device_id}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json().get("objectJson")

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

    def set_flat_boiler_powerful_mode_on(self, device_id):
        """
        Turn on the powerful mode of a flat boiler device.

        :param device_id: The device ID.
        :return: The response from the server.
        """
        url = f"{self.base_url}/api/flatboiler/setHeater"
        payload = {"deviceId": device_id, "heater": True}
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def set_flat_boiler_temperature(self, device_id, temperature):
        """
        Set the temperature of a flat boiler device.

        :param device_id: The device ID.
        :param temperature: The temperature to set.
        :return: The response from the server.
        """
        url = f"{self.base_url}/api/flatboiler/setTemperature"
        payload = {"deviceId": device_id, "temperature": temperature}
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
