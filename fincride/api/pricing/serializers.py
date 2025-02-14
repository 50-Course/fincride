from rest_framework import serializers


class FareRequestSerializer(serializers.Serializer):
    distance = serializers.FloatField(help_text="Estimated distance in KM")
    traffic_level = serializers.ChoiceField(choices=["low", "normal", "high"])
    demand_level = serializers.ChoiceField(
        choices=["normal", "peak"],
    )
    time_of_day = serializers.ChoiceField(
        choices=["morning", "evening", "night"],
        required=False,
    )


class FarePricingResponseSerializer(serializers.Serializer):
    base_fare = serializers.DecimalField(max_digits=10, decimal_places=2)
    distance_fare = serializers.DecimalField(max_digits=10, decimal_places=2)
    traffic_multiplier = serializers.DecimalField(max_digits=10, decimal_places=2)
    demand_multiplier = serializers.DecimalField(max_digits=10, decimal_places=2)
    time_factor = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_fare = serializers.DecimalField(max_digits=10, decimal_places=2)
