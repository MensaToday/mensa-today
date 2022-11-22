# Mensa Today Recommender System
Münster is a distributed University with various different canteens and bistros that serve different ranges of food which change every week. As a student who eats at those places frequently, you have to look through all of these dishes to find a meal you want to eat. The idea of our recommender system is to suggest meals based on various different factors: Your eating habits, location (based on semester schedule), weather,…).

## Setup Postgres Database
In order to be able to connect to the database inside of the docker container the environment variables have to be set correctly. Therefore create a `database-variables.env` file in the `mensa_recommend` directory. Copy the following environment variables into the .env file and change the variables respectively:

````
POSTGRES_DB = YOUR_DB_NAME
POSTGRES_USER = YOUR_DB_USER
POSTGRES_PASSWORD = YOUR_DB_PASSWORD
POSTGRES_HOST = db
POSTGRES_PORT = 5433

PGADMIN_DEFAULT_EMAIL = YOUR_PGADMIN_EMAIL
PGADMIN_DEFAULT_PASSWORD = YOUR_PGADMIN_PASSWORD
````

After creating the file start docker:

1. `docker-compose up`
2. In a seccond terminal connect to app container `docker exec -it mensa_recommend-app-1 bash`
3. `python manage.py makemigrations`
4. `python manage.py migrate`
5. `python manage.py createsuperuser`

Done now you can connect to your database.

## Notebooks
Jupyter notebooks for testing purposes can be created at the notbooks folder. Please follow the naming convetion: `initials-dd-mm-yyy-name_of_the_notebook`

## Data Structure
![erm](ERM.png)