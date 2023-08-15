import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime

def flight_search(departure_code, arrival_code, date):
    url = f"https://stub.amopromo.com.br/air/search/pzrvlDwoCwlzrWJmOzviqvOWtm4dkvuc/{departure_code}/{arrival_code}/{date}"
    basic_auth = requests.auth.HTTPBasicAuth('demo', 'swnvlD')
    response = requests.get(url, auth=basic_auth)

    # session = requests.Session()
    # retry = Retry(connect=3, backoff_factor=0.5)
    # adapter = HTTPAdapter(max_retries=retry)
    # session.mount('http://', adapter)
    # session.mount('https://', adapter)
    # session.get(url, auth=basic_auth)
    
    print(response.status_code)
    if not response.ok:
        print(response.content)
        #response.raise_for_status()
    else:
        return response.json()['options']

if __name__ == '__main__':
    today = datetime.today().date()
    #response = requests.get('https://stub.amopromo.com/air/search/pzrvlDwoCwlzrWJmOzviqvOWtm4dkvuc/MOC/CNF/2023-08-15')
    flights = flight_search('MOC', 'CNF', '2023-08-15')
    print(flights)