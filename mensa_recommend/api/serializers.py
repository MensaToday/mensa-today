from rest_framework import serializers
from mensa.models import DishPlan, Dish, Category, DishCategory, Mensa, UserDishRating, Additive, DishAdditive, Allergy, DishAllergy


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


class AdditiveSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "name"]
        model = Additive


class DishAdditiveSerializer(serializers.ModelSerializer):

    additive = AdditiveSerializer(
        read_only=True)

    class Meta:
        fields = ["additive"]
        model = DishAdditive


class AllergySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "name"]
        model = Allergy


class DishAllergySerializer(serializers.ModelSerializer):

    allergy = AllergySerializer(
        read_only=True)

    class Meta:
        fields = ["allergy"]
        model = DishAllergy


class DishSerializer(serializers.ModelSerializer):
    categories = serializers.ListSerializer(
        child=DishCategorySerializer(), source='dishcategory_set')
    additives = serializers.ListSerializer(
        child=DishAdditiveSerializer(), source='dishadditive_set')
    allergies = serializers.ListSerializer(
        child=DishAllergySerializer(), source='dishallergy_set')

    class Meta:
        fields = ["id", "categories", "additives", "allergies", "main", "name"]
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


class BasicDishSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ["id", "main", "name"]
        model = Dish


class UserDishRatingSerializer(serializers.ModelSerializer):

    dish = BasicDishSerializer(read_only=True)

    class Meta:
        fields = ["dish", "rating"]
        model = UserDishRating
