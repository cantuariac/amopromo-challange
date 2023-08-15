from datetime import datetime, timedelta

from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from airports.models import Airport

class SearchTest(TestCase):
    def setUp(self):
        Airport.objects.create(
            iata="MOC",
            city="Montes Claros",
            latitude=-16.707779,
            longitude=-43.817223,
            state="MG",
        )
        Airport.objects.create(
            iata="CNF",
            city="Belo Horizonte",
            latitude=-19.632418,
            longitude=-43.963215,
            state="MG",
        )

        user = User.objects.create_user("test_user", "", "*&g(*7g9g(G)")
        token = Token.objects.create(user=user)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_same_airport(self):
        response = self.client.get("/mock/search/MOC/MOC/2023-08-15/2023-8-16")

        self.assertContains(response, "'departure_code' and 'arrival_code' can't the same", status_code=400)

    def test_outbound_date(self):
        today = datetime.today().date()
        yesterday = today - timedelta(days = 1)
        response = self.client.get(f"/mock/search/MOC/CNF/{yesterday.strftime('%Y-%m-%d')}/{today.strftime('%Y-%m-%d')}")

        self.assertContains(response, "'outbound_date' can't be earlier than today", status_code=400)
    
    def test_return_date(self):
        today = datetime.today().date()
        yesterday = today - timedelta(days = 1)
        response = self.client.get(f"/mock/search/MOC/CNF/{today.strftime('%Y-%m-%d')}/{yesterday.strftime('%Y-%m-%d')}")

        self.assertContains(response, "'return_date' can't be earlier than 'outbound_date'", status_code=400)

    def test_airport_not_found(self):
        today = datetime.today().date().strftime('%Y-%m-%d')
        response = self.client.get(f"/mock/search/$$$/CNF/{today}/{today}")

        self.assertContains(response, "There is no airport with code: $$$", status_code=404)
        
        response = self.client.get(f"/mock/search/MOC/$$$/{today}/{today}")

        self.assertContains(response, "There is no airport with code: $$$", status_code=404)
