from decimal import Decimal
import enum

# This module uses explict typing to define the constants
# this ensures that changes to this module of invalid type is
# adequately reported by the type checker
#
# Morealso, this defrentiates it from "Magic Numbers" or anyone who thinks so


class TrafficLevel(enum.StrEnum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"


class DayTime(enum.StrEnum):
    MORNING = "morning"
    EVENING = "evening"
    NIGHT = "night"


class DemandLevel(enum.StrEnum):
    NORMAL = "normal"
    PEAK = "peak"


BASE_FARE: Decimal = Decimal(2.5)  # Fare is assumed in USD

BASE_SURGE_MULTIPLIER: Decimal = Decimal(1.2)
PEAK_SURGE_MULTIPLIER: Decimal = Decimal(2.0)

RATE_PER_KM: Decimal = Decimal(1.0)  # Rate is assumed in USD
TIME_FACTOR_MAP = {
    DayTime.MORNING: Decimal(1.0),
    DayTime.EVENING: Decimal(1.2),
    DayTime.NIGHT: Decimal(1.5),
}

TRAFFIC_MULTIPLIER_MAP = {
    TrafficLevel.LOW: Decimal(1.0),
    TrafficLevel.NORMAL: Decimal(1.2),
    TrafficLevel.HIGH: Decimal(1.5),
}
