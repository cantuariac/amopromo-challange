from django.urls import path
from airports.views import AirportsView

urlpatterns = [
    path('', AirportsView.as_view()),
]