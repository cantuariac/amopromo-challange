from datetime import datetime

from django.http import HttpRequest

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound, status

from airports.models import Airport
from mock_airlines.services import MockAirlinesService


class FlightSearchView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request:HttpRequest, departure_code, arrival_code, outbound_date, return_date):

        errors = []
        if departure_code == arrival_code:
            errors.append("'departure_code' and 'arrival_code' can't the same")
        if outbound_date < datetime.today().date():
            errors.append("'outbound_date' can't be earlier than today")
        if return_date < outbound_date:
            errors.append("'return_date' can't be earlier than 'outbound_date'")
        if errors:
            raise ValidationError({"detail":errors})
        
        departure_airport = Airport.objects.filter(iata=departure_code).first()
        if not departure_airport:
            raise NotFound(f"There is no airport with code: {departure_code}")
        
        arrival_airport = Airport.objects.filter(iata=arrival_code).first()
        if not arrival_airport:
            raise NotFound(f"There is no airport with code: {arrival_code}")
        
        options = MockAirlinesService.twoway_flights(departure_airport, arrival_airport, outbound_date, return_date)

        return Response(options)