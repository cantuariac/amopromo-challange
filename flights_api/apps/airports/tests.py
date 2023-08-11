from django.test import TestCase
from django.db.utils import IntegrityError
from airports.models import Airport

class AirportTestCase(TestCase):
    # def setUp(self):

    def test_iata_is_unique(self):
        Airport.objects.create(
            iata="MOC",
            city="Montes Claros",
            latitude=-16.707779,
            longitude=-43.817223,
            state="MG",
        )

        self.assertRaises(
            IntegrityError,
            lambda: Airport.objects.create(
                iata="MOC",
                city="Montes Claros",
                latitude=-16.707779,
                longitude=-43.817223,
                state="MG",
            ),
        )
