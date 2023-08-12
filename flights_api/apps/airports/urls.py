from django.urls import path
from airports.views import hello, AirportsView

urlpatterns = [
    path('', AirportsView.as_view()),
    path('hello/', hello),
]