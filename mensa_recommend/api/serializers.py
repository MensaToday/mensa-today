from rest_framework import serializers
from mensa.models import DishPlan, Dish, Category, DishCategory, Mensa


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "name"]
        model = Category


class DishCategorySerializer(serializers.ModelSerializer):

    category = CategorySerializer(
        read_only=True)

    class Meta:
        fields = ["category"]
        model = DishCategory


class DishSerializer(serializers.ModelSerializer):
    categories = serializers.ListSerializer(
        child=DishCategorySerializer(), source='dishcategory_set')

    class Meta:
        fields = ["id", "categories", "main", "name"]
        model = Dish


class MensaSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "name", "city", "street",
                  "houseNumber", "zipCode", "startTime", "endTime"]
        model = Mensa


class DishPlanSerializer(serializers.ModelSerializer):
    dish = DishSerializer(read_only=True)
    mensa = MensaSerializer(read_only=True)

    class Meta:
        fields = ["dish", "mensa", "date",
                  "priceStudent", "priceEmployee"]
        model = DishPlan
