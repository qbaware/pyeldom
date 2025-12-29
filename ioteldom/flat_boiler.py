import json
import aiohttp

from .constants import BASE_URL
from .models import Device
from .crc import crc32
from .crypto import encrypt
from .token_provider import TokenProvider
from .models import FlatBoilerDetails


class FlatBoilerClient:
    """
    Eldom flat boiler API client class.
    """

    def __init__(
        self,
        session: aiohttp.ClientSession,
        token_provider: TokenProvider,
    ):
        """
        Initialize the Eldom flat boiler API client.

        :param session: A session object.
        """
        self.session = session
        self.token_provider = token_provider

    async def get_flat_boiler_status(self, device: Device):
        """
        Get the status of a flat boiler device.

        :param device: The device.
        :return: The response from the server.
        """

        # Example curl request:
        #
        # curl \
        # -H "ionic-idd: <DEVICE_UUID>" \ # The 'ionic-idd' header is the device UUID, while the ID in the body is the device pair token, lol
        # -H "authorization: Bearer <TOKEN>" \
        # -H "user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0" \
        # -H "content-type: application/json" \
        # --data-binary "{\"Msg\":\"cXEdGfPnzi2BKP93KDtaHELl3Rfcp1EdeGLGPm3lIkH/eEfL1cV3KsaYpYQVUmM1h1ox4EaqC0yBk4u4WvBaQA==\"}" \
        # --compressed "https://iot.myeldom.com/api/direct-req"

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
        encrypted_payload = encrypt(payload)
        wrapped_payload = {"Msg": encrypted_payload}

        response = await self.session.post(url, json=wrapped_payload, headers=headers)
        response.raise_for_status()
        response_json = json.loads(await response.text())

        supported_heater_fields = {
            field.name for field in FlatBoilerDetails.__dataclass_fields__.values()
        }
        filtered_heater_json = {
            k: v for k, v in response_json.items() if k in supported_heater_fields
        }

        return FlatBoilerDetails(**filtered_heater_json)

    async def set_flat_boiler_state(self, device, state):
        """
        Set the state of a flat boiler device.

        :param device: The device.
        :param state: The state to set (an int) - 0 for Off, 2 for Powerful, 4 for Eco, 6 for Smart, 8 for ExtraSafe.
        :return: The response from the server.
        """

        # Example curl request:
        #
        # curl \
        # -H "ionic-idd: <DEVICE_UUID>" \ # The 'ionic-idd' header is the device UUID, while the ID in the body is the device pair token, lol
        # -H "authorization: Bearer <TOKEN>" \
        # -H "user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0" \
        # -H "content-type: application/json" \
        # --data-binary "{\"Msg\":\"cXEdGfPnzi2BKP93KDtaHELl3Rfcp1EdeGLGPm3lIkH/qVHRFecJV3wGPNbMxvsbKH8MtcU3Pe8JDw3ikdxL+/LX1k54uo0dnSnnnTA41yw=\"}" \
        # --compressed "https://iot.myeldom.com/api/direct-req"

        state_map = {
            0: "Off",
            2: "Powerfull",
            4: "Smart",
            6: "Eco",
            8: "ExtraSafe",
        }

        if state not in state_map:
            raise ValueError(f"Invalid state: {state}. Supported states (are the keys): {state_map}")

        url = f"{BASE_URL}/api/direct-req"
        headers = {
            "ionic-idd": device.uuid,
            "Authorization": f"Bearer {await self.token_provider.provide()}",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0",
            "Content-Type": "application/json",
        }

        payload = {
            "ID": device.pairTok,
            "Req": state_map.get(state),
            "CID": "1",
        }
        payload["CRC"] = crc32(payload)
        encrypted_payload = encrypt(payload)
        wrapped_payload = {"Msg": encrypted_payload}

        response = await self.session.post(url, json=wrapped_payload, headers=headers)
        response.raise_for_status()
