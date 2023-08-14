from datetime import datetime

from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response

from airports.models import Airport


class DateConverter:
    regex = '\d{4}-\d{1,2}-\d{1,2}'
    format = '%Y-%m-%d'

    def to_python(self, value):
        return datetime.strptime(value, self.format).date()

    def to_url(self, value):
        return value.strftime(self.format)

class SearchView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request, departure_airport, arrival_airport, departure_date, arrival_date):
        print(departure_airport, arrival_airport, departure_date, arrival_date)
        print(DateConverter().to_python(departure_date), DateConverter().to_python(arrival_date))
        return Response()