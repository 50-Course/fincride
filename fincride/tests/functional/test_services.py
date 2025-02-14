from decimal import Decimal

from django.test import TestCase

from fincride.api.pricing.constants import (BASE_FARE, BASE_SURGE_MULTIPLIER,
                                            NORMAL_SURGE_MULTIPLIER,
                                            PEAK_SURGE_MULTIPLIER, RATE_PER_KM,
                                            TRAFFIC_MULTIPLIER_MAP,
                                            TrafficLevel)
from fincride.api.pricing.services import FareEngine


class TestFareEngine(TestCase):
    def setUp(self):
        self.fare_engine = FareEngine()

    def test_standard_ride_fare(self):
        distance = 5
        traffic_level = "low"
        demand_level = "normal"
        time_of_day = None

        fare_data = self.fare_engine.calculate_fare(
            distance, traffic_level, demand_level, time_of_day
        )

        expected_fare = BASE_FARE + (distance * RATE_PER_KM)

        self.assertEqual(fare_data["distance_fare"], Decimal(5) * RATE_PER_KM)
        self.assertEqual(fare_data["traffic_multiplier"], Decimal(1.0))
        self.assertEqual(fare_data["demand_multiplier"], NORMAL_SURGE_MULTIPLIER)
        self.assertEqual(fare_data["total_fare"], expected_fare)

    def test_high_traffic_ride_fare(self):
        distance = 8
        traffic_level = "high"
        demand_level = "normal"
        time_of_day = None

        fare_data = self.fare_engine.calculate_fare(
            distance, traffic_level, demand_level, time_of_day
        )

        expected_fare = (BASE_FARE + (distance * RATE_PER_KM)) * Decimal(1.5)

        self.assertEqual(fare_data["base_fare"], BASE_FARE)
        self.assertEqual(fare_data["distance_fare"], 8 * RATE_PER_KM)
        self.assertEqual(fare_data["traffic_multiplier"], Decimal(1.5))
        self.assertEqual(fare_data["demand_multiplier"], NORMAL_SURGE_MULTIPLIER)
        self.assertEqual(fare_data["total_fare"], expected_fare)

    def test_surge_pricing_high_demand(self):
        distance = 12
        traffic_level = "normal"
        demand_level = "peak"
        time_of_day = None

        fare_data = self.fare_engine.calculate_fare(
            distance, traffic_level, demand_level, time_of_day
        )

        expected_fare = (
            (BASE_FARE + (distance * RATE_PER_KM))
            * Decimal(1.2)
            * PEAK_SURGE_MULTIPLIER
        )

        self.assertEqual(fare_data["base_fare"], BASE_FARE)
        self.assertEqual(fare_data["distance_fare"], 12 * RATE_PER_KM)
        self.assertEqual(
            fare_data["traffic_multiplier"],
            Decimal(1.2),
        )
        self.assertEqual(fare_data["demand_multiplier"], PEAK_SURGE_MULTIPLIER)
        self.assertEqual(fare_data["total_fare"], expected_fare)

    def test_peak_hour_with_high_traffic(self):
        distance = 7
        traffic_level = "high"
        demand_level = "peak"
        time_of_day = "evening"

        fare_data = self.fare_engine.calculate_fare(
            distance, traffic_level, demand_level, time_of_day
        )

        expected_fare = (
            (BASE_FARE + (7 * RATE_PER_KM))
            * Decimal(1.5)
            * PEAK_SURGE_MULTIPLIER
            * Decimal(1.3)
        )

        self.assertEqual(fare_data["base_fare"], BASE_FARE)
        self.assertEqual(fare_data["distance_fare"], 7 * RATE_PER_KM)
        self.assertEqual(fare_data["traffic_multiplier"], Decimal(1.5))
        self.assertEqual(fare_data["demand_multiplier"], PEAK_SURGE_MULTIPLIER)
        self.assertEqual(fare_data["time_factor"], Decimal(1.3))
        self.assertEqual(fare_data["total_fare"], expected_fare)

    def test_long_distance_ride(self):
        distance = 20
        traffic_level = "low"
        demand_level = "normal"
        time_of_day = None

        fare_data = self.fare_engine.calculate_fare(
            distance, traffic_level, demand_level, time_of_day
        )

        expected_fare = BASE_FARE + (20 * RATE_PER_KM)

        self.assertEqual(fare_data["base_fare"], BASE_FARE)
        self.assertEqual(fare_data["distance_fare"], 20 * RATE_PER_KM)
        self.assertEqual(fare_data["traffic_multiplier"], Decimal(1.0))
        self.assertEqual(fare_data["demand_multiplier"], NORMAL_SURGE_MULTIPLIER)
        self.assertEqual(fare_data["total_fare"], expected_fare)
