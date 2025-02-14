"""
Pricing Engine Module
Author: Eri A.

Created: 2025-02-13 22:32
"""

from decimal import Decimal
import enum
from typing import List, Dict

from api.pricing.constants import (
    BASE_FARE,
    BASE_SURGE_MULTIPLIER,
    PEAK_SURGE_MULTIPLIER,
    RATE_PER_KM,
    TIME_FACTOR_MAP,
    TRAFFIC_MULTIPLIER_MAP,
    DemandLevel,
)


# The algorithm
#
# Long distance ride:
#    - High distance, Low traffic, Normal demand = Base fare + per km rate
# Standard ride:
#   - Base fare + dist fare, no    Adjust the fare based on the time of day:
# High Traffic ride:
#  - Traffic multiplier applied to fare
# Peak hour + High traffic ride:
#   - Both traffic and dmeand multipliers are added
# Surge ride (High demand ride):
#   - Demand mulitplier appied to fare


class FareEngine:
    def __init__(
        self,
        base_fare: Decimal = BASE_FARE,
        surge_multiplier: Decimal = BASE_SURGE_MULTIPLIER,
        peak_surge_multiplier: Decimal = PEAK_SURGE_MULTIPLIER,
        rate_per_km: Decimal = RATE_PER_KM,
        time_factor_map: dict = TIME_FACTOR_MAP,
        traffic_multiplier_map: dict = TRAFFIC_MULTIPLIER_MAP,
    ):
        self.base_fare = base_fare
        self.surge_multiplier = surge_multiplier
        self.peak_surge_multiplier = peak_surge_multiplier
        self.rate_per_km = rate_per_km
        self.time_factor_map = time_factor_map
        self.traffic_multiplier_map = traffic_multiplier_map

    def calculate_fare(
        self,
        distance: int,
        traffic_level: str,
        demand_level: str,
        time_of_day: str | None = None,
    ) -> Dict[str, Decimal]:
        """
        Calculate the ride fare baseed on input parameters
        """

        total_fare = self.base_fare
        distance_fare = Decimal(distance) * self.rate_per_km

        # only adust fare, if traffic is high
        traffic_multiplier = self.traffic_multiplier_map.get(
            traffic_level, Decimal(1.0)
        )

        # next we want to apply the surge pricing
        # if the demand is high
        demand_multiplier = (
            self.peak_surge_multiplier
            if demand_level == DemandLevel.PEAK
            else Decimal(1.0)
        )

        time_factor = self.time_factor_map.get(time_of_day, Decimal(1.0))

        total_fare += distance_fare
        total_fare *= traffic_multiplier
        total_fare *= demand_multiplier
        total_fare *= time_factor

        return {
            "base_fare": self.base_fare,
            "distance_fare": distance_fare,
            "traffic_multiplier": traffic_multiplier,
            "demand_multiplier": demand_multiplier,
            "time_factor": time_factor,
            "total_fare": total_fare,
        }
