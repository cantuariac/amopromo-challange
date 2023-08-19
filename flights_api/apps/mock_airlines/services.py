from datetime import datetime
from itertools import product
import requests
import json

from airports.models import Airport
from mock_airlines.utils import DateConverter, haversine, duration_from_timestamps

def tmp_response(departure_code, arrival_code, date):
    try:
        res = json.load(open(f"./apps/mock_airlines/sample-response-{departure_code}-{arrival_code}-{DateConverter().to_url(date)}.json"))
    except FileNotFoundError:
        return []
    return res["options"]

class MockAirlinesService:

    @staticmethod
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
        flight_options = MockAirlinesService.flight_search(departure_airport.iata, arrival_airport.iata, flight_date)
        #flight_options = tmp_response(departure_airport.iata, arrival_airport.iata, flight_date)

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
                combination = {}
                combination["price"] = {
                    "fare": out["price"]["fare"] + ret["price"]["fare"],
                    "fee": out["price"]["fee"] + ret["price"]["fee"],
                    "total": out["price"]["total"] + ret["price"]["total"]
                }
                combination["outbound"] = out
                combination["return"] = ret
                flight_options.append(combination)

        return {
            "from": str(departure_airport),
            "to": str(arrival_airport),
            "outbound_date": outbound_date,
            "return_date": return_date,
            "options": sorted(flight_options, key=lambda x: x["price"]["total"])
        }