from drf_spectacular.utils import OpenApiExample

fare_pricing_request_example = OpenApiExample(
    name="Fare Request Example",
    request_only=True,
    value={
        "distance": 5.0,
        "time_of_day": "evening",
        "traffic_level": "low",
        "demand_level": "peak",
    },
)

fare_pricing_response_example = OpenApiExample(
    name="Fare Response Example",
    response_only=True,
    status_codes=[200],
    value={
        "data": {
            "base_fare": "2.50",
            "distance_fare": "5.00",
            "traffic_multiplier": "1.00",
            "demand_multiplier": "2.00",
            "time_factor": "1.30",
            "total_fare": "19.50",
        }
    },
)
