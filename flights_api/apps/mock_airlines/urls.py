from django.urls import path, register_converter

from mock_airlines.views import SearchView, DateConverter

register_converter(DateConverter, 'date')

urlpatterns = [
    path('search/<str:departure_code>/<str:arrival_code>/<date:outbound_date>/<date:return_date>', SearchView.as_view()),
]