from dataclasses import dataclass


@dataclass
class User:
    id: int
    """
    User ID.
    """
    login: str
    """
    Username.
    """
    email: str
    """
    Email.
    """


@dataclass
class Device:
    uuid: str
    """
    Device UUID. E.g., AD5B221071124F28
    """
    model: str
    """
    Device model. E.g., HTRCNV
    """
    fmodel: str
    """
    Another device model. This seems to be the actual device model. E.g., RH30NW
    """
    name: str
    """
    Device name. Seems to correlate with the FModel. E.g., RH30NW
    """
    pairTok: str
    """
    Pair token. Not really sure what a pair token is, but this is used in all API calls as the device ID. E.g., R7alOFhj9kDslr2X
    """


@dataclass
class ConvectorHeaterDetails:
    ID: str
    """
    Device pair token. This is the value that's used as device ID in the API calls. Yeah, the API is kind of odd.
    """
    T: str
    """
    Temperature reading. For 20 degrees, the value is 200.
    """
    TSet: str
    """
    Target temperature. For 19 degrees, use 190.
    """
    Status: str
    """
    Not sure what status is this.
    """
    Operation: str
    """
    Whether it's on or off. 16 - ON, 0 - OFF.
    """


@dataclass
class ConvectorHeaterStateChangeResponse:
    Res: str
    """
    Response status - "On", "Off", "SetParams", etc.
    """
    Code: str
    """
    Execution code - "0" for success.
    """
    Type: str
    """
    Type of response. E.g., "OK".
    """
    Reason: str
    """
    Reason for the response. E.g., "SUCCESS".
    """
