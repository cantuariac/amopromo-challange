# AmoPromo Challenge

## Description

### Endpoints

#### Authentication

Endpoint for API user's token generation.
```
curl --location 'http://127.0.0.1:8000/auth-token/' \
     --form 'username="<username>"' \
     --form 'password="<password>"'
```
```json
{
    "token": "<token>"
}
```
#### Airports

List available Airports
```
curl --location 'http://127.0.0.1:8000/airports' \
     --header 'Authorization: Token <token>'
```
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
#### Search

List available Airports
```
curl --location 'http://127.0.0.1:8000/mock/search/<departure_code>/<arrival_code>/<outbound_date>/<return_date>' \
     --header 'Authorization: Token <token>'
```
```json
{
    "from": "MOC (Montes Claros, MG)",
    "to": "CNF (Belo Horizonte, MG)",
    "outbound_date": "2023-08-30",
    "return_date": "2023-08-31",
    "options": [...]
}
```

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


## Technologies used