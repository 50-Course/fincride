from rest_framework.test import APITestCase
from rest_framework import status


class FarePricingAPIIntegrationTest(APITestCase):
    def test_standard_fare(self):
        url = "/api/calculate-fare/?distance=5&traffic_level=low&demand_level=normal"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["base_fare"], 2.5)
        self.assertEqual(response.data["data"]["distance_fare"], 5.0)
        self.assertEqual(response.data["data"]["traffic_multiplier"], 1.0)
        self.assertEqual(response.data["data"]["demand_multiplier"], 1.2)
        # self.assertEqual(response.data["data"]["total_fare"], 7.5)

    def test_high_traffic_pricing(self):
        url = "/api/calculate-fare/?distance=8&traffic_level=high&demand_level=normal"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["base_fare"], 2.5)
        self.assertEqual(response.data["data"]["distance_fare"], 8.0)
        self.assertEqual(response.data["data"]["traffic_multiplier"], 1.5)
        self.assertEqual(response.data["data"]["demand_multiplier"], 1.2)
        # self.assertEqual(response.data["data"]["total_fare"], 15.0)

    def test_surge_pricing_high_demand(self):
        url = "/api/calculate-fare/?distance=12&traffic_level=normal&demand_level=peak"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["base_fare"], 2.5)
        self.assertEqual(response.data["data"]["distance_fare"], 12.0)
        self.assertEqual(response.data["data"]["traffic_multiplier"], 1.0)
        self.assertEqual(response.data["data"]["demand_multiplier"], 2.0)
        # self.assertEqual(response.data["data"]["total_fare"], 28.5)

    def test_peak_hour_with_high_traffic(self):
        url = "/api/calculate-fare/?distance=7&traffic_level=high&demand_level=peak&time_of_day=evening"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["base_fare"], 2.5)
        self.assertEqual(response.data["data"]["distance_fare"], 7.0)
        self.assertEqual(response.data["data"]["traffic_multiplier"], 1.5)
        self.assertEqual(response.data["data"]["demand_multiplier"], 2.0)
        self.assertEqual(response.data["data"]["time_multiplier"], 1.3)
        # self.assertEqual(response.data["data"]["total_fare"], 41.4)

    def test_long_distance_ride(self):
        url = "/api/calculate-fare/?distance=20&traffic_level=low&demand_level=normal"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["base_fare"], 2.5)
        self.assertEqual(response.data["data"]["distance_fare"], 20.0)
        self.assertEqual(response.data["data"]["traffic_multiplier"], 1.0)
        self.assertEqual(response.data["data"]["demand_multiplier"], 1.2)
        # self.assertEqual(response.data["data"]["total_fare"], 22.5)
