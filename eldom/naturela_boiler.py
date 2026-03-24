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

    async def set_naturela_boiler_temperature(self, device_id, temperature):
        """
        Set the target temperature of a Naturela boiler device.

        Fetches the full current state, updates the target temperature, and saves
        the full state back to the server (the API requires the complete payload).

        :param device_id: The device ID (integer).
        :param temperature: The target temperature to set.
        :return: The response from the server.
        """
        get_url = f"{BASE_URL}/api/boiler/{device_id}"
        get_response = await self.session.get(get_url)
        get_response.raise_for_status()
        response_json = json.loads(await get_response.text())
        boiler_json = json.loads(response_json.get("objectJson"))

        alarms = [
            {
                "listeners": {},
                "validateTime": True,
                "daysEnabled": alarm["DaysEnabled"],
                "step": 1,
                "id": alarm["ID"],
                "enabled": alarm["Enabled"],
                "begin": alarm["Begin"],
                "end": alarm["End"],
                "temperature": alarm["Temperature"],
            }
            for alarm in boiler_json.get("Alarms", [])
        ]

        payload = {
            "listeners": {},
            "INVALID_TEMPERATURE": -128,
            "formid": device_id,
            "alarms": alarms,
            "elSetTemp": temperature,
            "heaterOnTemp": boiler_json.get("HeaterOnTemp"),
            "sensor": boiler_json.get("Sensor"),
            "rate1Start": boiler_json.get("Rate1Start"),
            "rate2Start": boiler_json.get("Rate2Start"),
            "solarDT1On": boiler_json.get("SolarDT1On"),
            "solarDT1Off": boiler_json.get("SolarDT1Off"),
            "DHWPriorityDT2On": boiler_json.get("DHWPriorityDT2On"),
            "DHWPriorityDT2Off": boiler_json.get("DHWPriorityDT2Off"),
            "CHPriorityT4On": boiler_json.get("CHPriorityT4On"),
            "CHPriorityT4Off": boiler_json.get("CHPriorityT4Off"),
            "BoilerPumpPriority": boiler_json.get("BoilerPumpPriority"),
            "elHeaterKw": boiler_json.get("ElHeaterKW"),
            "elHeater": boiler_json.get("ElHeater"),
            "solarColector": boiler_json.get("SolarColector"),
            "boilerHeatingInstalation": boiler_json.get("BoilerHeatingInstalation"),
            "anode": boiler_json.get("Anode"),
            "antiLegionella": boiler_json.get("AntiLegionella"),
            "solarAntiFrost": boiler_json.get("SolarAntiFrost"),
            "solarAntiFrostTemperature": boiler_json.get("SolarAntiFrostTemperature"),
            "autoHolidayMode": boiler_json.get("AutoHolidayMode"),
            "useBoilerPump": boiler_json.get("UseBoilerPump"),
            "tankMinTemp": boiler_json.get("TankMinTemp"),
            "solarOverheating": boiler_json.get("SolarOverheating"),
            "deviceId": boiler_json.get("DeviceID"),
            "state": boiler_json.get("State"),
            "HardwareVersion": boiler_json.get("HardwareVersion"),
            "SoftwareVersion": boiler_json.get("SoftwareVersion"),
            "hardwareGroup": 2,
        }

        save_url = f"{BASE_URL}/api/boiler/save"
        save_response = await self.session.post(save_url, json=payload)
        save_response.raise_for_status()

    async def reset_naturela_boiler_energy_usage(self, device_id):
        """
        Reset the energy usage of a Naturela boiler device.

        :param device_id: The device ID.
        :return: The response from the server.
        """
        url = f"{BASE_URL}/api/boiler/resetEnergyDate"
        payload = {"deviceId": device_id}
        response = await self.session.post(url, json=payload)
        response.raise_for_status()
