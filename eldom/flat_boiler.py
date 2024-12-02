import json
import aiohttp

from eldom.models import FlatBoilerDetails


class FlatBoilerClient:
    """
    Eldom flat boiler API client abstract class.

    Before using the client, you need to login with the login method.
    """

    def __init__(
        self,
        base_url: str,
        session: aiohttp.ClientSession,
    ):
        """
        Initialize the Eldom flat boiler API client.

        Make sure to login with the login method before using the other methods of the client.

        :param base_url: The base URL for the API.
        :param session: A session object.
        """
        if type(self) is FlatBoilerClient:
            raise NotImplementedError(
                "FlatBoilerClient is an abstract class and cannot be instantiated directly"
            )

        self.base_url = base_url
        self.session = session

    async def get_flat_boiler_status(self, device_id):
        """
        Get the status of a flat boiler device.

        :param device_id: The device ID.
        :return: The response from the server.
        """
        url = f"{self.base_url}/api/flatboiler/{device_id}"
        response = await self.session.get(url)
        response.raise_for_status()
        response_json = json.loads(await response.text())
        boiler_json = json.loads(response_json.get("objectJson"))

        supported_boiler_fields = {
            field.name for field in FlatBoilerDetails.__dataclass_fields__.values()
        }
        filtered_boiler_json = {
            k: v for k, v in boiler_json.items() if k in supported_boiler_fields
        }

        return FlatBoilerDetails(**filtered_boiler_json)

    async def set_flat_boiler_state(self, device_id, state):
        """
        Set the state of a flat boiler device.

        :param device_id: The device ID.
        :param state: The state to set (e.g., 0 to turn off, 1 to turn on heating, 2 to turn on Smart mode, 3 to turn on Study mode).
        :return: The response from the server.
        """
        url = f"{self.base_url}/api/flatboiler/setState"
        payload = {"deviceId": device_id, "state": state}
        response = await self.session.post(url, json=payload)
        response.raise_for_status()

    async def set_flat_boiler_powerful_mode_on(self, device_id):
        """
        Turn on the powerful mode of a flat boiler device.

        :param device_id: The device ID.
        :return: The response from the server.
        """
        url = f"{self.base_url}/api/flatboiler/setHeater"
        payload = {"deviceId": device_id, "heater": True}
        response = await self.session.post(url, json=payload)
        response.raise_for_status()

    async def set_flat_boiler_temperature(self, device_id, temperature):
        """
        Set the temperature of a flat boiler device.

        :param device_id: The device ID.
        :param temperature: The temperature to set.
        :return: The response from the server.
        """
        url = f"{self.base_url}/api/flatboiler/setTemperature"
        payload = {"deviceId": device_id, "temperature": temperature}
        response = await self.session.post(url, json=payload)
        response.raise_for_status()
