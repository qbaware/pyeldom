from dataclasses import dataclass
from typing import Optional
from enum import Enum


class Language(Enum):
    ENGLISH = 0


@dataclass
class User:
    id: int
    firstName: str
    lastName: str
    email: str
    IsAdmin: bool
    alertEmail: Optional[str]
    language: Language
    lastLoginDate: str
    lastActiveDate: str
    isActive: bool
    agreedWithTerms: bool
    ip: str


@dataclass
class Device:
    id: int
    realDeviceId: str
    deviceType: int
    name: Optional[str]
    isOwner: bool
    ownerId: int
    ownerName: str
    hwVersion: int
    swVersion: int
    usersWithAccess: int
    lastDataRefreshDate: str
    timeZoneId: Optional[str]
    timeZoneName: Optional[str]


@dataclass
class FlatBoilerDetails:
    ID: int
    DeviceID: str
    Type: int
    Protocol: int
    Manifactor: int
    HardwareVersion: int
    SoftwareVersion: int
    SaveLocked: bool
    LastRefreshDate: str
    EnergyDate: str
    SetTemp: int
    OnOffStat: int
    State: int
    PowerFlag: int
    FirstCylinderOn: bool
    SecondCylinderOn: bool
    STL_Temp: int
    FT_Temp: int
    WHHeat: int
    EnergyD: float
    EnergyN: float
    AllowSeasonCompensation: bool
    SmartControlState: int
    Volume: int
    AllowTwoHeaters: bool
    HorizontalBoiler: bool
    HeatingState: int
    SelfLearningCNT: int
    SavedEnergy: int
    Heater: bool
    LoweredPower: bool
    FrostProtection: bool
    HasBoost: bool


@dataclass
class SmartBoilerDetails:
    ID: int
    DeviceID: str
    Type: int
    Protocol: int
    Manifactor: int
    HardwareVersion: int
    SoftwareVersion: int
    SaveLocked: bool
    LastRefreshDate: str
    EnergyDate: str
    Heater: bool
    WH_TempL: int
    EnergyD: float
    EnergyN: float
    SmartBoilerControl: int
    Compensation: bool
    State: int
    SetTemp: int
    ErrorFlag: int
    BoostHeating: bool
    SavedEnergy: int


@dataclass
class ConvectorHeaterDetails:
    ID: int
    DeviceID: str
    Type: int
    Protocol: int
    Manifactor: int
    HardwareVersion: int
    SoftwareVersion: int
    SaveLocked: bool
    LastRefreshDate: str
    EnergyD: float
    EnergyN: float
    State: int
    SetTemp: int
    AmbientTemp: int
    Power: int
    BoostHeating: bool
    OpenWindow: int
    PowerIDX: int
    PCBTemp: int
    ErrorFlag: int
