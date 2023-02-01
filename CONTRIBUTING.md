# Contribution

## Notebooks
Jupyter notebooks for testing purposes can be created at the notbooks folder. Please follow the naming convetion: `initials-dd-mm-yyy-name_of_the_notebook`

## Code Documentation Template

Every class/method documentation should consist of the following elements:
- A short description of the class/method
- A description of input parameters:
  - Parametername : Type
    - Short description
- A description of output parameters:
  - Parametername : Type
    - Short description

```Python
class DishRecommender:
    """
        The dish recommender class is the main class for generating
        recommendations. As of right now, the approach is held very naive
        without any inbetween savings to speed up the process in any way.

        To increase performance, the recommender caches operations that are
        time-consuming and updates them only if their conditions changes.
        Still, for the first execution a recommendation takes up to 2 seconds
        but for all following invocations the recommender returns predictions
        after 0.1 seconds. For more information about the conditions, check
        their classes.
    """
    
    def __init__(self, user: User, day: date, entire_week: bool = False):
        """
            user : User
                The user for whom recommendations should be generated. This is
                important as we use content-based filtering and therefore
                recommend dishes based on previous ratings.
            day : date
                The day that should be recommended for.
            entire_week : bool
                If true, the method predict() returns predictions for the
                entire week. Otherwise, only recommendations for the day that
                was specified before are generated.
        """
        pass

    def predict(self, recommendations_per_day: int = 1,
                serialize: bool = False) -> Dict[date, List[
            Tuple[DishPlan, float]]]:
        """Predicting recommendations for a user. This process is efficient
        and can be executed synchronously without any problems.

        Parameters
        ----------
        recommendations_per_day : int
            The number of recommendations per day. Must be > 0. Default is 1.
        serialize: bool
            Whether DishPlan instances should be directly serialized.

        Return
        ------
        result : Dict[date, List[Tuple[DishPlan, float]]]
            The result per day encapsulated in a dict saved by the date
            itself. The list of recommendations per day is structured by a
            tuple combining the DishPlan (with information about dish, mensa
            and date) and the prediction value (0 <= p <= 1).
        """
        pass
```

# Setup

## Setup Postgres Database

In order to be able to connect to the database inside of the docker container the environment variables have to be set correctly. Therefore create a `database-variables.env` file in the `mensa_recommend` directory. Copy the following environment variables into the .env file and change the variables respectively:

```
POSTGRES_DB = YOUR_DB_NAME
POSTGRES_USER = YOUR_DB_USER
POSTGRES_PASSWORD = YOUR_DB_PASSWORD
POSTGRES_HOST = db
POSTGRES_PORT = 5433

PGADMIN_DEFAULT_EMAIL = YOUR_PGADMIN_EMAIL
PGADMIN_DEFAULT_PASSWORD = YOUR_PGADMIN_PASSWORD
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
DEEPL_KEY = YOUR_API_KEY
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
GOOGLE_API_KEY = YOUR_API_KEY             # currently not required
GOOGLE_PROJECT_CX = YOUR_PROJECT_CX_KEY   # currently not required
PRIVATE_KEY = YOUR_PRIVATE_KEY
HTTP_PROXY=http://wwwproxy.uni-muenster.de:3128
HTTPS_PROXY=http://wwwproxy.uni-muenster.de:3128
DEEPL_KEY = YOUR_API_KEY
```
