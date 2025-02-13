from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from fincride.api.pricing.serializers import FareRequestSerializer
from fincride.api.pricing.services import FareEngine


class FarePricingView(APIView):
    """
    Calculate the fare pricing for a given ride
    """

    def get(self, request):
        serializer = FareRequestSerializer(data=request.query_params)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        distance = serializer.validated_data["distance"]
        traffic_level = serializer.validated_data["traffic_level"]
        demand_level = serializer.validated_data["demand_level"]
        time_of_day = serializer.validated_data.get("time_of_day", None)

        pricing_engine = FareEngine()
        fare_data = pricing_engine.calculate_fare(
            distance=distance,
            traffic_level=traffic_level,
            demand_level=demand_level,
            time_of_day=time_of_day,
        )

        response_serializer = FarePricingResponseSerializer(data=fare_data)

        return Response(
            {
                "data": response_serializer.data,
            },
            status=status.HTTP_200_OK,
        )
