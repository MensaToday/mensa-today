[![Python 3.9.7](https://img.shields.io/badge/python-3.9-orange.svg)](https://www.python.org/downloads/release/python-390/) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) ![GitHub version](https://img.shields.io/github/v/release/erikzimmermann/mensa-today?color=green&include_prereleases)

# <img src="https://github.com/erikzimmermann/mensa-today/blob/development/frontend/src/assets/logo.png" height="24" style="margin-right:5px;"/><span>MensaToday - your dish recommender in Münster</span>

Münster is a distributed University with various different canteens and bistros that serve different ranges of food which change every week. As a student who eats at those places frequently, you have to look through all of these dishes to find a meal you want to eat. The idea of our recommender system is to suggest meals based on various different factors: Your eating habits, location (based on semester schedule), weather, ….

![Poster](poster.svg)
## Contributing
See [our contributing guidelines](https://github.com/erikzimmermann/mensa-today/blob/development/CONTRIBUTING.md) for detailed information about testing, documentation and project setup.

```
POSTGRES_DB = YOUR_DB_NAME
POSTGRES_USER = YOUR_DB_USER
POSTGRES_PASSWORD = YOUR_DB_PASSWORD
POSTGRES_HOST = db
POSTGRES_PORT = 5433

PGADMIN_DEFAULT_EMAIL = YOUR_PGADMIN_EMAIL
PGADMIN_DEFAULT_PASSWORD = YOUR_PGADMIN_PASSWORD
SCRIPT_NAME=pg # when used behind nginx
```

After creating the file start docker:

1. `docker-compose up`
2. In a seccond terminal connect to app container `docker exec -it mensa-today_app_1 bash`
3. `python manage.py makemigrations`
4. `python manage.py migrate`
5. `python manage.py createsuperuser`

Done now you can connect to your database.

## Environment files

To run the local as well as production environment specific environment files has to be created. For the local development create a `local-variables.env` file in the root directory that should contain the following:

```
VUE_APP_BASE_URL = YOUR_URL
GOOGLE_API_KEY = YOUR_API_KEY             # currently not required
GOOGLE_PROJECT_CX = YOUR_PROJECT_CX_KEY   # currently not required
```

For development the `VUE_APP_BASE_URL = http://localhost:9999/api/v1/` and for production `VUE_APP_BASE_URL = http://10.14.28.50:9999`
For the Production see next section.

## Production

To deploy the django app use the `docker-compose-prod.yaml` file. This file requires a `prod-variables.env` file which have to be create:

```
SECRET_KEY = foo
DEBUG = False
JWT_EXPIRATION_DELTA = 10800
PRODUCTION = True
PROXY = True
GOOGLE_API_KEY = YOUR_API_KEY             # currently not required
GOOGLE_PROJECT_CX = YOUR_PROJECT_CX_KEY   # currently not required
PRIVATE_KEY = YOUR_PRIVATE_KEY
HTTP_PROXY=http://wwwproxy.uni-muenster.de:3128
HTTPS_PROXY=http://wwwproxy.uni-muenster.de:3128
```

## Notebooks

Jupyter notebooks for testing purposes can be created at the notbooks folder. Please follow the naming convetion: `initials-dd-mm-yyy-name_of_the_notebook`

## Celery

Celery is an open source asynchronous task queue or job queue which is based on distributed message passing. While it supports scheduling, its focus is on operations in real time. Celery is used in combination with the message broker redis. For more information, see [Celery docs](https://docs.celeryq.dev/en/stable/).

## Data Structure
last updated on 30th December 2022
![erm](ERM.png)
