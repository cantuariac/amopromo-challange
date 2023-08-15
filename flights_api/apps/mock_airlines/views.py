from datetime import datetime
from itertools import product

from django.shortcuts import render
from django.http import HttpRequest

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound, status

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from airports.models import Airport

import json
def tmp_response(departure_code, arrival_code, date):
    try:
        res = json.load(open(f"./apps/mock_airlines/{departure_code}-{arrival_code}-{DateConverter().to_url(date)}.json"))
    except FileNotFoundError:
        res = []
    return res

class DateConverter:
    regex = "\d{4}-\d{1,2}-\d{1,2}"
    format = "%Y-%m-%d"

    def to_python(self, value):
        return datetime.strptime(value, self.format).date()

    def to_url(self, value):
        return value.strftime(self.format)


# from https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r

def duration_from_timestamps(ts_start, ts_end):
    tdelta = datetime.fromisoformat(ts_end) - datetime.fromisoformat(ts_start)
    return tdelta.total_seconds() / 3600

class MockAirlinesService:

    @staticmethod
    # TODO: BROKEN
    def flight_search(departure_code, arrival_code, date):
        url = f"https://stub.amopromo.com.br/air/search/pzrvlDwoCwlzrWJmOzviqvOWtm4dkvuc/{departure_code}/{arrival_code}/{DateConverter().to_url(date)}"
        basic_auth = requests.auth.HTTPBasicAuth("demo", "swnvlD")
        response = requests.get(url, auth=basic_auth)

        if not response.ok:
            print(response.content)
            #response.raise_for_status()
        else:
            return response.json()["options"]

    @staticmethod
    def oneway_flights(departure_airport:Airport, arrival_airport:Airport, flight_date:datetime):
        # TODO: replace tmp_response with flight_search
        flight_options = tmp_response(departure_airport.iata, arrival_airport.iata, flight_date)

        for flight in flight_options:
            fare = flight["price"]["fare"]
            fee = max(fare * 0.1, 40.0)
            total = fare+fee
            flight["price"] = {
                "fare": fare,
                "fee":fee,
                "total": total
            }

            _range = haversine(departure_airport.longitude, departure_airport.latitude, arrival_airport.longitude, arrival_airport.latitude)
            duration = duration_from_timestamps(flight["departure_time"], flight["arrival_time"])
            flight["meta"]={
                "range": _range,
                "cruise_speed_kmh": _range/duration,
                "cost_per_km": total/_range
            }
        
        return flight_options

    @staticmethod
    def twoway_flights(departure_airport, arrival_airport, outbound_date, return_date):

        outbound_flights = MockAirlinesService.oneway_flights(departure_airport, arrival_airport, outbound_date)
        return_flights = MockAirlinesService.oneway_flights(arrival_airport, departure_airport, return_date)
        
        flight_options = []
        for out, ret in product(outbound_flights, return_flights):
            if out["arrival_time"] < ret["departure_time"]:
                flight_options.append({
                    "outbound": out,
                    "return": ret
                })

        return {
            "outbound_date": outbound_date,
            "return_date": return_date,
            "options": flight_options
            }

class SearchView(APIView):
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