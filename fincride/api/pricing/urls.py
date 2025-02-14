from django.urls import path

from .views import FarePricingView

urlpatterns = [
    path("calculate-fare/", FarePricingView.as_view(), name="calculate_fare"),
]
