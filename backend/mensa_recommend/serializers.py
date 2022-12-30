from rest_framework import serializers
import mensa.models as mensa_model
import users.models as user_model


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "name"]
        model = mensa_model.Category


class DishCategorySerializer(serializers.ModelSerializer):

    category = CategorySerializer(
        read_only=True)

    class Meta:
        fields = ["category"]
        model = mensa_model.DishCategory


class AdditiveSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "name"]
        model = mensa_model.Additive


class DishAdditiveSerializer(serializers.ModelSerializer):

    additive = AdditiveSerializer(
        read_only=True)

    class Meta:
        fields = ["additive"]
        model = mensa_model.DishAdditive


class AllergySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "name"]
        model = mensa_model.Allergy


class DishAllergySerializer(serializers.ModelSerializer):

    allergy = AllergySerializer(
        read_only=True)

    class Meta:
        fields = ["allergy"]
        model = mensa_model.DishAllergy


class DishSerializer(serializers.ModelSerializer):
    categories = serializers.ListSerializer(
        child=DishCategorySerializer(read_only=True), source='dishcategory_set')
    additives = serializers.ListSerializer(
        child=DishAdditiveSerializer(read_only=True), source='dishadditive_set')
    allergies = serializers.ListSerializer(
        child=DishAllergySerializer(read_only=True), source='dishallergy_set')

    class Meta:
        fields = ["id", "categories", "additives",
                  "allergies", "main", "name", "url"]
        model = mensa_model.Dish


class MensaSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "name", "city", "street",
                  "houseNumber", "zipCode", "startTime", "endTime"]
        model = mensa_model.Mensa


class ExtRatingsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "rating_avg", "rating_count"]
        model = mensa_model.ExtDishRating


class DishPlanSerializer(serializers.ModelSerializer):
    dish = DishSerializer(read_only=True)
    mensa = MensaSerializer(read_only=True)
    ext_ratings = serializers.SerializerMethodField(
        method_name="get_ext_ratings")
    user_ratings = serializers.SerializerMethodField(
        method_name="get_user_ratings")
    side_dishes = serializers.SerializerMethodField(
        method_name="get_side_dishes")
    side_selected = serializers.SerializerMethodField(
        method_name="get_side_selected")

    class Meta:
        fields = ["dish", "ext_ratings", "user_ratings", "mensa", "date",
                  "priceStudent", "priceEmployee", "side_dishes", "side_selected"]
        model = mensa_model.DishPlan

    def __init__(self, *args, **kwargs):
        """"
            Decide which fields should be returned based on the context
            When the context 'include_sides' is True then side dishes should be included.
            When the context 'sides' is True then a boolean side_selected will be included that
            states if the side dish was selected by the user or not. If the context is false the
            coresponding fields will be deleted.
        """
        super(DishPlanSerializer, self).__init__(*args, **kwargs)

        if 'include_sides' in self.context:
            if not self.context['include_sides']:
                del self.fields['side_dishes']
        else:
            del self.fields['side_dishes']

        if 'sides' in self.context:
            if not self.context['sides']:
                del self.fields['side_selected']
            else:
                del self.fields['mensa']
                del self.fields['date']
        else:
            del self.fields['side_selected']

    def get_ext_ratings(self, obj):
        ext_ratings = mensa_model.ExtDishRating.objects.filter(
            mensa=obj.mensa).filter(dish=obj.dish).latest("date")

        return ExtRatingsSerializer(ext_ratings, read_only=True).data

    def get_user_ratings(self, obj):
        user_ratings = mensa_model.UserDishRating.objects.filter(
            dish=obj.dish).filter(user=self.context["user"])

        return UserRatingsWithoutDishSerializer(user_ratings, read_only=True, many=True).data

    def get_side_dishes(self, obj):
        side_dishes = mensa_model.DishPlan.objects.filter(
            mensa=obj.mensa, date=obj.date, dish__main=False).all()

        return DishPlanSerializer(side_dishes, read_only=True, many=True, context={
            'user': self.context['user'], 'include_sides': False, 'sides': True, 'main': obj}).data

    def get_side_selected(self, obj):
        print(obj.id)
        try:
            user_side_selection = mensa_model.UserSideSelection.objects.get(
                user=self.context['user'], main=self.context['main'], side=obj)

            return True
        except mensa_model.UserSideSelection.DoesNotExist:
            return False


class BasicDishSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ["id", "main", "name"]
        model = mensa_model.Dish


class UserRatingsWithoutDishSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ["rating"]
        model = mensa_model.UserDishRating


class UserDishRatingSerializer(serializers.ModelSerializer):

    dish = BasicDishSerializer(read_only=True)

    class Meta:
        fields = ["dish", "rating"]
        model = mensa_model.UserDishRating


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ["username", "card_id"]
        model = user_model.User
