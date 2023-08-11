# Backend User organization development
This is a Django project which primarily builds APIs using Django REST Framework.

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

## Documentations

- [SWAGGER](http://127.0.0.1:8000/swagger/) <br>
- [REDOC](http://127.0.0.1:8000/redoc/)
