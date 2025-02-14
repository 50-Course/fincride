from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# we would be using string heres because django recognizes decimal as strings


class FarePricingAPIIntegrationTest(APITestCase):
    def test_standard_fare(self):
        url = reverse("calculate_fare")
        response = self.client.get(
            url, {"distance": 5, "traffic_level": "low", "demand_level": "normal"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["base_fare"], "2.50")
        self.assertEqual(response.data["data"]["distance_fare"], "5.00")
        self.assertEqual(response.data["data"]["traffic_multiplier"], "1.00")
        self.assertEqual(response.data["data"]["demand_multiplier"], "1.00")
        self.assertEqual(response.data["data"]["total_fare"], "7.50")

    def test_high_traffic_pricing(self):
        url = reverse("calculate_fare")
        response = self.client.get(
            url, {"distance": 8, "traffic_level": "high", "demand_level": "normal"}
        )

        expected_fare = (Decimal(2.5) + (Decimal(8) * Decimal(1.0))) * Decimal(1.5)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["base_fare"], "2.50")
        self.assertEqual(response.data["data"]["distance_fare"], "8.00")
        self.assertEqual(response.data["data"]["traffic_multiplier"], "1.50")
        self.assertEqual(response.data["data"]["demand_multiplier"], "1.00")
        self.assertEqual(
            response.data["data"]["total_fare"],
            str(expected_fare.quantize(Decimal("0.01"))),
        )

    def test_surge_pricing_high_demand(self):
        url = reverse("calculate_fare")
        response = self.client.get(
            url, {"distance": 12, "traffic_level": "normal", "demand_level": "peak"}
        )

        expected_fare = (
            (Decimal(2.5) + (Decimal(12) * Decimal(1.0))) * Decimal(1.2) * Decimal(2.0)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["base_fare"], "2.50")
        self.assertEqual(response.data["data"]["distance_fare"], "12.00")
        self.assertEqual(response.data["data"]["traffic_multiplier"], "1.20")
        self.assertEqual(response.data["data"]["demand_multiplier"], "2.00")
        self.assertEqual(
            response.data["data"]["total_fare"],
            str(expected_fare.quantize(Decimal("0.01"))),
        )

    def test_peak_hour_with_high_traffic(self):
        url = reverse("calculate_fare")
        response = self.client.get(
            url,
            {
                "distance": 7,
                "traffic_level": "high",
                "demand_level": "peak",
                "time_of_day": "evening",
            },
        )

        expected_fare = (
            (Decimal(2.5) + (Decimal(7) * Decimal(1.0)))
            * Decimal(1.5)
            * Decimal(2.0)
            * Decimal(1.3)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["base_fare"], "2.50")
        self.assertEqual(response.data["data"]["distance_fare"], "7.00")
        self.assertEqual(response.data["data"]["traffic_multiplier"], "1.50")
        self.assertEqual(response.data["data"]["demand_multiplier"], "2.00")
        self.assertEqual(response.data["data"]["time_factor"], "1.30")
        self.assertEqual(
            response.data["data"]["total_fare"],
            str(expected_fare.quantize(Decimal("0.01"))),
        )

    def test_long_distance_ride(self):
        url = reverse("calculate_fare")
        response = self.client.get(
            url, {"distance": 20, "traffic_level": "low", "demand_level": "normal"}
        )

        expected_fare = Decimal(2.5) + (Decimal(20) * Decimal(1.0))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["base_fare"], "2.50")
        self.assertEqual(response.data["data"]["distance_fare"], "20.00")
        self.assertEqual(response.data["data"]["traffic_multiplier"], "1.00")
        self.assertEqual(response.data["data"]["demand_multiplier"], "1.00")
        self.assertEqual(
            response.data["data"]["total_fare"],
            str(expected_fare.quantize(Decimal("0.01"))),
        )
