# Django Backend using DRF

## Clone project

```
git clone https://github.com/muhtor/user-organization.git
```
and `pull` from remote git:
```
git pull origin dev
```

## Installation and run

### Create a virtual environment
* Create a virtual environment in the root project directory


- Windows OS – `python -m venv venv` <br>
- Mac or Linux OS – `python3 -m venv venv`

... and activate venv

### Installing requirements

```
pip install -r requirements.txt
```

### Run project
user-organization\src> `python manage.py runserver`


---

## API Endpoint (auth)

### Getting auth token
```
http://127.0.0.1:8000/api/v1/auth-token/create/
```

If using Postman POST the following data into "Body -> raw (json)".

```
{
  "email": "user@example.com",
  "password": "12345678i"
}
```

Response:
```
{
    "success": true,
    "message": "OK",
    "results": {
        "refresh": "RefreshTokenToGetAccessTokenSinceAccessTokenExpiresEvery5Minutes",
        "access": "AccessTokenWhichIsGivenInHTTPHeaderToAuthenticateUser"
    }
}
```

### Getting auth token using refresh token
```
http://127.0.0.1:8000/api/v1/auth-token/refresh/
```

If using Postman POST the following data into "Body -> raw (json)".

```
{
  "refresh": "<RefreshToken>",
}
```

Response:
```
{
    "access" : "AccessTokenWhichIsGivenInHTTPHeaderToAuthenticateUser"
}
```

### Django test commands

```
python manage.py test apps
```
or
```
python manage.py test apps accounts
```

# DOCKER

first you need to switch docker branch

```
git checkout docker
```
and
```
git pull origin docker
```

### Run with `docker-compose.yml`
user-organization\src> `docker compose up`

### Commands
Running migrations with docker-compose (if `run` is used instead of `exec`, then new container is created instead of using the existing one - hence it's better to use `exec`)
```
docker-compose exec orgweb python manage.py makemigrations
docker-compose exec orgweb python manage.py migrate
docker-compose exec orgweb python manage.py createsuperuser
docker-compose exec orgweb python manage.py test apps accounts
```
if you want to go inside the container
```
docker exec -it orgweb bash
```
and you can easily run manage.py

```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py test apps accounts
```

### Other commands

Deleting all images and containers (dangerous please use it with caution)
```
docker system prune -a --volumes
```

```
docker images
docker container ls
```

## Documentations

- [SWAGGER](http://127.0.0.1:8000/swagger/) <br>
- [REDOC](http://127.0.0.1:8000/redoc/)
