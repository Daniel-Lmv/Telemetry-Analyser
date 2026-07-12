from enum import Enum, auto


class TelemetryFeature(Enum):
    SESSION_TIME = auto()
    LAP = auto()
    LAP_TIME = auto()
    LAP_DISTANCE = auto()
    BEST_LAP_TIME = auto()
    BEST_SECTOR_1_TIME = auto()
    BEST_SECTOR_2_TIME = auto()

    THROTTLE = auto()
    BRAKE = auto()
    STEERING = auto()
    CLUTCH = auto()
    GEAR = auto()

    SPEED = auto()
    RPM = auto()
    FUEL = auto()
    FUEL_USED = auto()

    TYRE_WEAR = auto()
    TYRE_PRESSURE = auto()
    TYRE_TEMPERATURE = auto()
    TYRE_COMPOUND = auto()

    BRAKE_TEMPERATURE = auto()
    TRACK_TEMPERATURE = auto()

    DRS = auto()
    ERS = auto()
    BATTERY = auto()

    IN_PITS = auto()

    GPS_LATITUDE = auto()
    GPS_LONGITUDE = auto()
