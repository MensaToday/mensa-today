from users.models import User
from mensa.models import Category, UserCategory, Allergy, UserAllergy


def save_preferences(user: User, categories: list[str], allergies: list[str]):
    """Wrapper function to save categories and allergies

    Parameters
    ----------
    user : User
        User object
    categories : list
        List of categories as strings
    allergies : list
        List of allergies as strings
    """

    save_categories(user, categories)
    save_allergies(user, allergies)


def save_categories(user: User, categories: list[str]):
    """Function to save categories

    Parameters
    ----------
    user : User
        User object
    categories : list
        List of categories as strings
    """

    if len(categories) == 0:
        categorie_objects = Category.objects.all()
    else:
        categorie_objects = []
        for category in categories:
            try:
                category_object = Category.objects.get(
                    name=category)

                categorie_objects.append(category_object)
            except:
                pass

    for co in categorie_objects:
        UserCategory(user=user, category=co).save()


def save_allergies(user: User, allergies: list[str]):
    """Function to save allergies

    Parameters
    ----------
    user : User
        User object
    allergies : list
        List of allergies as strings
    """

    allergies_objects = []
    for allergy in allergies:
        try:
            allergy_object = Allergy.objects.get(name=allergy)
            allergies_objects.append(allergy_object)
        except:
            pass

    for ao in allergies_objects:
        UserAllergy(user=user, allergy=ao).save()
