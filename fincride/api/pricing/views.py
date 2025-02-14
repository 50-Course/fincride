from api.pricing.serializers import (FarePricingResponseSerializer,
                                     FareRequestSerializer)
from api.pricing.services import FareEngine
from drf_spectacular.utils import (OpenApiParameter, OpenApiRequest,
                                   OpenApiResponse, extend_schema)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .openapi import (fare_pricing_request_example,
                      fare_pricing_response_example)


class FarePricingView(APIView):
    """
    Calculate the fare pricing for a given ride
    """

    @extend_schema(
        tags=["Pricing"],
        summary="Get Fare Pricing",
        description="Request the fare price for a ride based on the distance, traffic level, demand level and time of day.",
        parameters=[
            OpenApiParameter(
                name="distance",
                description='Destination in km e.g "5"',
                type=int,
            ),
            OpenApiParameter(
                name="traffic_level",
                type=str,
                description='Traffic level e.g "low", "normal", "high"',
            ),
            OpenApiParameter(
                name="demand_level",
                type=str,
                description="Demand level i.e rush hour - 'normal', 'peak' ",
            ),
            OpenApiParameter(
                name="time_of_day",
                type=str,
                required=False,
                description='Time of day e.g "morning", "evening", "night"',
            ),
        ],
        request=OpenApiRequest(
            FareRequestSerializer, examples=[fare_pricing_request_example]
        ),
        responses={
            200: OpenApiResponse(
                FarePricingResponseSerializer,
                "Price retrieve successfully",
                examples=[fare_pricing_response_example],
            ),
            400: OpenApiResponse(description="Bad Request"),
            500: OpenApiResponse(
                description="Internal Server Error e.g server is down or database error"
            ),
        },
    )
    def get(self, request):
        serializer = FareRequestSerializer(data=request.query_params)
        if serializer.is_valid():
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

            response_serializer = FarePricingResponseSerializer(fare_data)

            return Response(
                {
                    "data": response_serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
