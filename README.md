# Backend Baraka ERP development
This is a Django project which primarily builds APIs using Django REST Framework.

### How to clone project

```
https://gitlab.com/baraka-erp/baraka-backend.git
```
## Guide for developers
Developers do not have direct access to master branch. Only the maintainer has access to master. Develops need to push to the branch 'dev'. The maintainer merges 'dev' with 'master' if need be.

Create 'dev' branch:
```
git branch dev
```

Activate 'dev' branch as by default 'master' is activate:
```
git checkout dev
```

See which branch is active:
```
git branch
```

Commit to local git:
```
git commit -m "Changes made to this app with some details"
```

Push commits to remote git:
```
git push origin dev
```

Pull from remote git:
```
git pull origin dev
```

## OTHERS

---
## API ENDPOINTS

### Getting auth token
```
https://api.baraka.site.uz/auth-token/create/
```

If using Postman POST the following form data into "Body -> x-www-form-urlencoded".

|Key     | Value          |
|--------|:--------------:|
|email   |test@email.com  |
|password|TestPassWord    |

Response:
```
{
    "refresh": "RefreshTokenToGetAccessTokenSinceAccessTokenExpiresEvery5Minutes",
    "access" : "AccessTokenWhichIsGivenInHTTPHeaderToAuthenticateUser"
}
```

### Getting auth token using refresh token
```
https://api.baraka.site.uz/auth-token/refresh/
```

If using Postman POST the following form data into "Body -> x-www-form-urlencoded".

|Key     | Value          |
|--------|:--------------:|
|refresh   |RefreshTokenToGetAccessTokenSinceAccessTokenExpiresEvery5Minutes  |

Response:
```
{
    "access" : "AccessTokenWhichIsGivenInHTTPHeaderToAuthenticateUser"
}
```

### Check auth token using access token
```
GET > https://api.baraka.site.uz/api/accounts/v1/me/
```

Response:
```
{
    "username": "John",
    "email": john@test.com,
    "first_name": John,
    "last_name": Deo,
    "fullname": john deo,
    "phone": +9989012345
}
```

### Registration
```
https://api.baraka.site.uz/api/accounts/v1/create/
```

POST this json to register a user ("Body -> raw" (data type JSON) on Postman):
```
{
    "username": "John",
    "email": john@test.com,
    "first_name": John,
    "last_name": Deo,
    "fullname": john deo,
    "phone": +9989012345
}
```

Response:
```
{
    "username": "John",
    "email": john@test.com,
    "first_name": John,
    "last_name": Deo,
    "fullname": john deo,
    "phone": +9989012345
}
```

# DOCKER

### Django commands
Running migrations with docker-compose (if `run` is used instead of `exec`, then new container is created instead of using the existing one - hence it's better to use `exec`)
```
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic
docker-compose exec web python manage.py createsuperuser
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

