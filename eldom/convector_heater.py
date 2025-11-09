import json
import aiohttp

from .constants import BASE_URL
from .models import ConvectorHeaterDetails


class ConvectorHeaterClient:
    """
    Eldom Convector heater API client abstract class.

    Before using the client, you need to login with the login method.
    """

    def __init__(
        self,
        session: aiohttp.ClientSession,
    ):
        """
        Initialize the Eldom convector heater API client.

        Make sure to login with the login method before using the other methods of the client.

        :param session: A session object.
        """
        self.session = session

    async def get_convector_heater_status(self, device_id):
        """
        Get the status of a convector heater device.

        :param device_id: The device ID.
        :return: The response from the server.
        """
        url = f"{BASE_URL}/api/panelconvector/{device_id}"
        response = await self.session.get(url)
        response.raise_for_status()
        response_json = json.loads(await response.text())
        heater_json = json.loads(response_json.get("objectJson"))

        supported_heater_fields = {
            field.name for field in ConvectorHeaterDetails.__dataclass_fields__.values()
        }
        filtered_heater_json = {
            k: v for k, v in heater_json.items() if k in supported_heater_fields
        }

        return ConvectorHeaterDetails(**filtered_heater_json)

    async def set_convector_heater_state(self, device_id, state):
        """
        Set the state of a convector heater device.

        :param device_id: The device ID.
        :param state: The state to set (e.g., 0 to turn off, 1 to turn on heating, 2 to turn on Smart mode, 3 to turn on Study mode).
        :return: The response from the server.
        """
        url = f"{BASE_URL}/api/panelconvector/setState"
        payload = {"deviceId": device_id, "state": state}
        response = await self.session.post(url, json=payload)
        response.raise_for_status()

    async def set_convector_heater_temperature(self, device_id, temperature):
        """
        Set the temperature of a convector heater device.

        :param device_id: The device ID.
        :param temperature: The temperature to set.
        :return: The response from the server.
        """
        url = f"{BASE_URL}/api/panelconvector/setTemperature"
        payload = {"deviceId": device_id, "temperature": temperature}
        response = await self.session.post(url, json=payload)
        response.raise_for_status()
