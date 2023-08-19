# AmoPromo Challenge

## Description

Project made as a software development test for an AmoPromo's job application.

⚠️ **Warning:** This is not a real or production ready web application.

**flights_api** is a RESTful Web API for serving available two way flight options between two airports. This API makes an integration with two external services, **Domestic Airports API** for consulting Airport data and **Mock Airlines Inc API** for searching flights offered by a fictional airlines company.

## Setup

A development environment for this project can be run and tested using a Docker container. [Install Docker](https://docs.docker.com/get-docker/) before starting.

On the root directory of the repository, run this command to create and start the container:
 ```
docker compose up -d
 ```

After the build is finished, open a shell inside the container:

 ```
docker exec -it <container-name-or-id> sh
 ```

On the container's shell, run this command to apply database migrations:

 ```
python manage.py migrate
 ```

Create a super user with:

 ```
python manage.py createsuperuser
 ```

To run the provided tests execute:

 ```
python manage.py test
 ```

Now  you should be able to login on [Django's Admin page](http://127.0.0.1:8000/admin) for the project.

## Usage

### Import airports command

Django command to cache airport info from Domestic Airports API into a local database.

```sh
python manage.py import_airports
```

### Authentication

**POST** endpoint for user's API Token generation.

Sample request:
```
curl --location 'http://127.0.0.1:8000/auth-token/' \
     --form 'username="<username>"' \
     --form 'password="<password>"'
```

Sample response:
```json
{
    "token": "<token>"
}
```
### Airports

**GET** endpoint to list available Airports

Sample request:
```
curl --location 'http://127.0.0.1:8000/airports' \
     --header 'Authorization: Token <token>'
```

Sample response:
```json
[
    {
        "iata": "AAX",
        "city": "Araxa",
        "state": "MG"
    },
    {
        "iata": "AFL",
        "city": "Alta Floresta",
        "state": "MT"
    },
    ...
]
```
### Search

**GET** endpoint to search two way flight options between airports.

URL must be constructed in this format `/mock/search/<departure_code>/<arrival_code>/<outbound_date>/<return_date>`:
- departure_code - departure airport iata code, regex: [A-Z]{3}
- arrival_code - arrival airport iata code, regex: [A-Z]{3}
- outbound_date - departure date for outbound flight, using the following format: YYYY-mm-dd
- return_date - departure date for return flight, using the following format: YYYY-mm-dd

Sample request:
```
curl --location 'http://127.0.0.1:8000/mock/search/MOC/CNF/2023-08-30/2023-8-31' \
     --header 'Authorization: Token <token>'
```

Sample response:
```json
{
    "from": "MOC (Montes Claros, MG)",
    "to": "CNF (Belo Horizonte, MG)",
    "outbound_date": "2023-08-30",
    "return_date": "2023-08-31",
    "options": [
        {
            "price": {
                "fare": 306.09,
                "fee": 80.0,
                "total": 386.09
            },
            "outbound": {
                "departure_time": "2023-08-30T21:15:00",
                "arrival_time": "2023-08-30T21:57:00",
                "price": {
                    "fare": 167.7,
                    "fee": 40.0,
                    "total": 207.7
                },
                "aircraft": {
                    "model": "ATR-72",
                    "manufacturer": "Alenia"
                },
                "meta": {
                    "range": 325.57048138718716,
                    "cruise_speed_kmh": 465.10068769598166,
                    "cost_per_km": 0.6379570995350503
                }
            },
            "return": {
                "departure_time": "2023-08-31T02:00:00",
                "arrival_time": "2023-08-31T02:29:00",
                "price": {
                    "fare": 138.39,
                    "fee": 40.0,
                    "total": 178.39
                },
                "aircraft": {
                    "model": "Dash 8",
                    "manufacturer": "Bombardier"
                },
                "meta": {
                    "range": 325.57048138718716,
                    "cruise_speed_kmh": 673.5940994217665,
                    "cost_per_km": 0.5479305102843409
                }
            }
        },
        ...
    ]
}
```

## Technologies used

### Django

This project was made using Django web framework, version 3.2.

### Django REST framework

This toolkit was used to standardize views' responses and authentication access.

### Requests

The Requests python library was used to perform HTTP calls from the project.