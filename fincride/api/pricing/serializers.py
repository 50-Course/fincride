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
