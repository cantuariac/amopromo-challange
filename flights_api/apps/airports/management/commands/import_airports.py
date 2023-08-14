from django.core.management.base import BaseCommand, CommandError
import requests

from airports.models import Airport


class DomesticAirportsAPI:
    @staticmethod
    def get_airports():
        basic_auth = requests.auth.HTTPBasicAuth('demo', 'swnvlD')
        response = requests.get(
            'https://stub.amopromo.com/air/airports/pzrvlDwoCwlzrWJmOzviqvOWtm4dkvuc',
            auth=basic_auth,
        )

        if not response.ok:
            response.raise_for_status()
        else:
            return response.json().values()


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        try:
            airports_data = DomesticAirportsAPI.get_airports()

            for data in airports_data:
                Airport.objects.update_or_create(
                    iata=data['iata'],
                    city=data['city'],
                    state=data['state'],
                    latitude=data['lat'],
                    longitude=data['lon'],
                )

        except Exception as ex:
            raise CommandError(ex)
        else:
            self.stdout.write(self.style.SUCCESS('Airport list updated'))
