import requests

class DomesticAirportsAPI:
    @staticmethod
    def get_airports():
        basic_auth = requests.auth.HTTPBasicAuth("demo", "swnvlD")
        response = requests.get(
            "https://stub.amopromo.com/air/airports/pzrvlDwoCwlzrWJmOzviqvOWtm4dkvuc",
            auth=basic_auth,
        )

        if not response.ok:
            response.raise_for_status()
        else:
            return response.json().values()