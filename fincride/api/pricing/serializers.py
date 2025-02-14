from django.db import models
from rest_framework import serializers


class FareRequestSerializer(serializers.Serializer):
    class TrafficLevelChoices(models.TextChoices):
        LOW = "low", "Low"
        NORMAL = "normal", "Normal"
        HIGH = "high", "High"

    class DemandLevelChoices(models.TextChoices):
        NORMAL = "normal", "Normal"
        PEAK = "peak", "Peak"

    class TimeOfDayChoices(models.TextChoices):
        MORNING = "morning", "Morning"
        EVENING = "evening", "Evening"
        NIGHT = "night", "Night"

    distance = serializers.IntegerField(help_text="Estimated distance in KM")
    traffic_level = serializers.ChoiceField(choices=TrafficLevelChoices.choices)
    demand_level = serializers.ChoiceField(
        choices=DemandLevelChoices.choices,
    )
    time_of_day = serializers.ChoiceField(
        choices=TimeOfDayChoices.choices,
        required=False,
    )


class FarePricingResponseSerializer(serializers.Serializer):
    base_fare = serializers.DecimalField(max_digits=10, decimal_places=2)
    distance_fare = serializers.DecimalField(max_digits=10, decimal_places=2)
    traffic_multiplier = serializers.DecimalField(max_digits=10, decimal_places=2)
    demand_multiplier = serializers.DecimalField(max_digits=10, decimal_places=2)
    time_factor = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_fare = serializers.DecimalField(max_digits=10, decimal_places=2)
