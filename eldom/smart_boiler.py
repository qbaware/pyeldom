import json
import aiohttp

from .constants import BASE_URL
from .models import SmartBoilerDetails


class SmartBoilerClient:
    """
    Eldom smart boiler API client abstract class.

    Before using the client, you need to login with the login method.
    """

    def __init__(
        self,
        session: aiohttp.ClientSession,
    ):
        """
        Initialize the Eldom smart boiler API client.

        Make sure to login with the login method before using the other methods of the client.

        :param session: A session object.
        """
        self.session = session

    async def get_smart_boiler_status(self, device_id):
        """
        Get the status of a smart boiler device.

        :param device_id: The device ID.
        :return: The response from the server.
        """
        url = f"{BASE_URL}/api/smartboiler/{device_id}"
        response = await self.session.get(url)
        response.raise_for_status()
        response_json = json.loads(await response.text())
        boiler_json = json.loads(response_json.get("objectJson"))

        supported_boiler_fields = {
            field.name for field in SmartBoilerDetails.__dataclass_fields__.values()
        }
        filtered_boiler_json = {
            k: v for k, v in boiler_json.items() if k in supported_boiler_fields
        }

        return SmartBoilerDetails(**filtered_boiler_json)

    async def set_smart_boiler_state(self, device_id, state):
        """
        Set the state of a smart boiler device.

        :param device_id: The device ID.
        :param state: The state to set (e.g., 0 to turn off, 1 to turn on heating, 2 to turn on Smart mode, 3 to turn on Study mode).
        :return: The response from the server.
        """
        url = f"{BASE_URL}/api/smartboiler/setState"
        payload = {"deviceId": device_id, "state": state}
        response = await self.session.post(url, json=payload)
        response.raise_for_status()

    async def set_smart_boiler_powerful_mode_on(self, device_id):
        """
        Turn on the powerful mode of a smart boiler device.

        :param device_id: The device ID.
        :return: The response from the server.
        """
        url = f"{BASE_URL}/api/smartboiler/setHeater"
        payload = {"deviceId": device_id, "heater": True}
        response = await self.session.post(url, json=payload)
        response.raise_for_status()

    async def set_smart_boiler_temperature(self, device_id, temperature):
        """
        Set the temperature of a smart boiler device.

        :param device_id: The device ID.
        :param temperature: The temperature to set.
        :return: The response from the server.
        """
        url = f"{BASE_URL}/api/smartboiler/setTemperature"
        payload = {"deviceId": device_id, "temperature": temperature}
        response = await self.session.post(url, json=payload)
        response.raise_for_status()

    async def reset_smart_boiler_energy_usage(self, device_id):
        """
        Reset the energy usage of a smart boiler device.

        :param device_id: The device ID.
        :return: The response from the server.
        """
        url = f"{BASE_URL}/api/smartboiler/resetEnergyDate"
        payload = {"deviceId": device_id}
        response = await self.session.post(url, json=payload)
        response.raise_for_status()
