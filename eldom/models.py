from dataclasses import dataclass
import datetime
from typing import Optional
from enum import Enum


class Language(Enum):
    ENGLISH = 0


@dataclass(frozen=True)
class User:
    id: int
    firstName: str
    lastName: str
    email: str
    IsAdmin: bool
    alertEmail: Optional[str]
    language: Language
    lastLoginDate: datetime
    lastActiveDate: datetime
    isActive: bool
    agreedWithTerms: bool
    ip: str


@dataclass(frozen=True)
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
    lastDataRefreshDate: datetime
    timeZoneId: Optional[str]
    timeZoneName: Optional[str]


@dataclass(frozen=True)
class FlatBoilerDetails:
    ID: int
    DeviceID: str
    Type: int
    Protocol: int
    Manifactor: int
    HardwareVersion: int
    SoftwareVersion: int
    SaveLocked: bool
    LastRefreshDate: datetime
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


@dataclass(frozen=True)
class SmartBoilerDetails:
    ID: int
    DeviceID: str
    Type: int
    Protocol: int
    Manifactor: int
    HardwareVersion: int
    SoftwareVersion: int
    SaveLocked: bool
    LastRefreshDate: datetime
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
