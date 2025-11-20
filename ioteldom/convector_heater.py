import json
import aiohttp

from .constants import BASE_URL
from .models import ConvectorHeaterDetails, ConvectorHeaterStateChangeResponse, Device
from .crc import crc32
from .token_provider import TokenProvider


class ConvectorHeaterClient:
    """
    Eldom Convector heater API client.

    Before using the client, you need to login with the login method.
    """

    def __init__(
        self,
        session: aiohttp.ClientSession,
        token_provider: TokenProvider,
    ):
        """
        Initialize the Eldom convector heater API client.

        Make sure to login with the login method before using the other methods of the client.

        :param session: A session object.
        :param token_provider: A token provider object.
        """
        self.session = session
        self.token_provider = token_provider

    async def get_convector_heater_status(self, device: Device):
        """
        Get the status of a convector heater device.

        :param device: The device object.
        :return: The response from the server.
        """

        # Example curl request:
        # curl -H "ionic-idd: <DEVICE_UUID>" -H "authorization: Bearer <TOKEN>" -H "user-agent: Mozilla/5.0 (Linux; Android 14; sdk_gphone64_arm64 Build/UE1A.230829.050; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/113.0.5672.136 Mobile Safari/537.36" -H "content-type: application/json" --data-binary "{\"ID\":\"R7alOFhj9kDslr2X\",\"Req\":\"GetStatus\",\"CID\":\"1\",\"CRC\":\"DD80A782\"}" --compressed "https://iot.myeldom.com/api/direct-req"

        # Notes: The 'ionic-idd' header is the device UUID, while the ID in the body is the device pair token, lol

        url = f"{BASE_URL}/api/direct-req"
        headers = {
            "ionic-idd": device.uuid,
            "Authorization": f"Bearer {await self.token_provider.provide()}",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0",
            "Content-Type": "application/json",
        }

        payload = {
            "ID": device.pairTok,
            "Req": "GetStatus",
            "CID": "1",
        }
        payload["CRC"] = crc32(payload)

        response = await self.session.post(url, json=payload, headers=headers)
        response.raise_for_status()
        response_json = json.loads(await response.text())

        supported_heater_fields = {
            field.name for field in ConvectorHeaterDetails.__dataclass_fields__.values()
        }
        filtered_heater_json = {
            k: v for k, v in response_json.items() if k in supported_heater_fields
        }

        return ConvectorHeaterDetails(**filtered_heater_json)

    async def set_convector_heater_state(self, device: Device, state: int):
        """
        Set the state of a convector heater device.

        States can either be ON (16) or OFF (0).

        :param device: The device object.
        :param state: The state to set (e.g., 0 to turn off, 16 to turn on).
        :return: The response from the server.
        """

        # Example curl request:
        # curl -H -H "ionic-idd: <DEVICE_UUID>" -H "authorization: Bearer <TOKEN>" -H "user-agent: Mozilla/5.0 (Linux; Android 14; sdk_gphone64_arm64 Build/UE1A.230829.050; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/113.0.5672.136 Mobile Safari/537.36" -H "content-type: application/json" --data-binary "{\"ID\":\"R7alOFhj9kDslr2X\",\"Req\":\"On\",\"CID\":\"1\",\"CRC\":\"81D7BD02\"}" --compressed "https://iot.myeldom.com/api/direct-req"

        # Notes: The 'ionic-idd' header is the device UUID, while the ID in the body is the device pair token

        states_map = {0: "Off", 16: "On"}

        url = f"{BASE_URL}/api/direct-req"
        headers = {
            "ionic-idd": device.uuid,
            "Authorization": f"Bearer {await self.token_provider.provide()}",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0",
            "Content-Type": "application/json",
        }

        payload = {
            "ID": device.pairTok,
            "Req": states_map[state],
            "CID": "1",
        }
        payload["CRC"] = crc32(payload)

        response = await self.session.post(url, json=payload, headers=headers)
        response.raise_for_status()
        response_json = json.loads(await response.text())

        supported_heater_fields = {
            field.name
            for field in ConvectorHeaterStateChangeResponse.__dataclass_fields__.values()
        }
        filtered_heater_json = {
            k: v for k, v in response_json.items() if k in supported_heater_fields
        }

        return ConvectorHeaterStateChangeResponse(**filtered_heater_json)

    async def set_convector_heater_temperature(self, device: Device, temperature: int):
        """
        Set the temperature of a convector heater device.

        :param device: The device object.
        :param temperature: The temperature to set. Use an integer value (e.g., 22 for 22C).
        :return: The response from the server.
        """

        # Example curl request:
        # curl -H "ionic-idd: <DEVICE_UUID>" -H "authorization: Bearer <TOKEN>" -H "user-agent: Mozilla/5.0 (Linux; Android 14; sdk_gphone64_arm64 Build/UE1A.230829.050; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/113.0.5672.136 Mobile Safari/537.36" -H "content-type: application/json" --data-binary "{\"ID\":\"R7alOFhj9kDslr2X\",\"Req\":\"SetParams\",\"TSet\":\"22\",\"AutoTimeSet\":\"1\",\"Rate1\":\"06:00\",\"Rate2\":\"22:00\",\"SystemSettings\":\"1, 2, 2, 0\",\"Lock\":\"0\",\"CID\":\"1\",\"CRC\":\"1A61D4E8\"}" --compressed "https://iot.myeldom.com/api/direct-req"

        # Notes: The 'ionic-idd' header is the device UUID, while the ID in the body is the device pair token

        url = f"{BASE_URL}/api/direct-req"
        headers = {
            "ionic-idd": device.uuid,
            "Authorization": f"Bearer {await self.token_provider.provide()}",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0",
            "Content-Type": "application/json",
        }

        payload = {
            "ID": device.pairTok,
            "Req": "SetParams",
            "TSet": str(temperature),

            # TODO: Find and replace those parameters with their actual current values instead of hardcoding.
            "AutoTimeSet": "1",
            "Rate1": "06:00",
            "Rate2": "22:00",
            "SystemSettings": "1, 2, 2, 0",
            "Lock": "0",

            "CID": "1",
        }
        payload["CRC"] = crc32(payload)

        response = await self.session.post(url, json=payload, headers=headers)
        response.raise_for_status()
        response_json = json.loads(await response.text())

        supported_heater_fields = {
            field.name
            for field in ConvectorHeaterStateChangeResponse.__dataclass_fields__.values()
        }
        filtered_heater_json = {
            k: v for k, v in response_json.items() if k in supported_heater_fields
        }

        return ConvectorHeaterStateChangeResponse(**filtered_heater_json)
