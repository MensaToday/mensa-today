# data-integration-recommender
Recommender System in Python using Django

## Setup Postgres Database
In order to be able to connect to the databse inside of the docker container the environment variables have to be set correctly. Therefore create a `database-variables.env` file in the `mensa_recommend` directory. Copy the following environment variables into the .env file and change the variables respectively:

````
POSTGRES_DB = YOUR_DB_NAME
POSTGRES_USER = YOUR_DB_USER
POSTGRES_PASSWORD = YOUR_DB_PASSWORD
POSTGRES_HOST = db
POSTGRES_PORT = 5433

PGADMIN_DEFAULT_EMAIL = YOUR_PGADMIN_EMAIL
PGADMIN_DEFAULT_PASSWORD = YOUR_PGADMIN_PASSWORD
````