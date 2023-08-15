from django.core.management.base import BaseCommand, CommandError

from airports.models import Airport
from airports.services import DomesticAirportsAPI


class Command(BaseCommand):
    help = "Updates local airport info from Domestic Airports API"

    def handle(self, *args, **options):
        try:
            airports_data = DomesticAirportsAPI.get_airports()

            for data in airports_data:
                Airport.objects.update_or_create(
                    iata=data["iata"],
                    city=data["city"],
                    state=data["state"],
                    latitude=data["lat"],
                    longitude=data["lon"],
                )

        except Exception as ex:
            raise CommandError(ex)
        else:
            self.stdout.write(self.style.SUCCESS("Airport list updated"))
