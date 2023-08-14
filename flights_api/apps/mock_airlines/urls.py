from django.urls import path, register_converter

from mock_airlines.views import SearchView, DateConverter

register_converter(DateConverter, 'date')

urlpatterns = [
    path('search/<str:departure_airport>/<str:arrival_airport>/<date:departure_date>/<date:arrival_date>', SearchView.as_view()),
]