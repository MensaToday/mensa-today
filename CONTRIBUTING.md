## Contribution

### Code Documentation Template

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
