from django.urls import path

from apps.mock_airlines.views import SearchView

urlpatterns = [
    path('search/<str:departure_airport>/<str:arrival_airport>/<str:departure_date>/<str:arrival_date>', SearchView.as_view()),
]