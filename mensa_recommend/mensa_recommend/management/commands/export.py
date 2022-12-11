from django.core.management.base import BaseCommand

from mensa.models import Dish


class Command(BaseCommand):
    """
        This command can be used to export all currently stored dishes for
        experiments.
    """

    def handle(self, *args, **options):
        dishes = []
        for dish in Dish.objects.all():
            categories = [o.id for o in dish.categories.all()]
            additives = [o.id for o in dish.additives.all()]
            allergies = [o.id for o in dish.allergies.all()]
            dishes.append((dish.id, dish.name, categories, additives,
                           allergies, dish.main))
        print(dishes)
