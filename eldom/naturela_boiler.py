import json
import aiohttp

from .constants import BASE_URL
from .models import NaturelaBoilerDetails


class NaturelaBoilerClient:
    """
    Eldom Naturela boiler API client.

    Before using the client, you need to login with the login method.
    """

    def __init__(
        self,
        session: aiohttp.ClientSession,
    ):
        """
        Initialize the Eldom Naturela boiler API client.

        Make sure to login with the login method before using the other methods of the client.

        :param session: A session object.
        """
        self.session = session

    async def get_naturela_boiler_status(self, device_id):
        """
        Get the status of a Naturela boiler device.

        :param device_id: The device ID.
        :return: The response from the server.
        """
        url = f"{BASE_URL}/api/boiler/{device_id}"
        response = await self.session.get(url)
        response.raise_for_status()
        response_json = json.loads(await response.text())
        boiler_json = json.loads(response_json.get("objectJson"))

        supported_boiler_fields = {
            field.name for field in NaturelaBoilerDetails.__dataclass_fields__.values()
        }
        filtered_boiler_json = {
            k: v for k, v in boiler_json.items() if k in supported_boiler_fields
        }

        return NaturelaBoilerDetails(**filtered_boiler_json)

    async def set_naturela_boiler_state(self, device_id, state):
        """
        Set the state of a Naturela boiler device.

        :param device_id: The device ID.
        :param state: The state to set (0 = Off, 1 = On, 2 = Holiday) as an int.
        :return: The response from the server.
        """
        url = f"{BASE_URL}/api/boiler/setState"
        payload = {"deviceId": device_id, "state": state}
        response = await self.session.post(url, json=payload)
        response.raise_for_status()

    async def set_naturela_boiler_powerful_mode_on(self, device_id):
        """
        Turn on the powerful mode (heater) of a Naturela boiler device.

        :param device_id: The device ID.
        :return: The response from the server.
        """
        url = f"{BASE_URL}/api/boiler/setHeater"
        payload = {"deviceId": device_id, "heater": True}
        response = await self.session.post(url, json=payload)
        response.raise_for_status()
