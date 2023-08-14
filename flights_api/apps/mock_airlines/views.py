from datetime import datetime

from django.shortcuts import render

import rest_framework
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from airports.models import Airport

from django.http import HttpRequest

class DateConverter:
    regex = '\d{4}-\d{1,2}-\d{1,2}'
    format = '%Y-%m-%d'

    def to_python(self, value):
        return datetime.strptime(value, self.format).date()

    def to_url(self, value):
        return value.strftime(self.format)

class MockAirlinesService:
    @staticmethod
    def twoway_search(departure_code, arrival_code, departure_date, arrival_date):
        departure_airport = Airport.objects.filter(iata=departure_code).first()
        arrival_airport = Airport.objects.filter(iata=arrival_code).first()

        return [str(departure_airport), str(arrival_airport)]

class SearchView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request:HttpRequest, departure_airport, arrival_airport, departure_date, arrival_date):

        errors = []
        if departure_airport == arrival_airport:
            errors.append("'departure_airport' and 'arrival_airport' can't the same")
        if departure_date < datetime.today().date():
            errors.append("'departure_date' can't be earlier than today")
        if arrival_date< departure_date:
            errors.append("'arrival_date' can't be earlier than 'departure_date'")
        
        if errors:
            raise ValidationError(errors)
        
        options = MockAirlinesService.twoway_search(departure_airport, arrival_airport, departure_date, arrival_date)

        return Response(options)