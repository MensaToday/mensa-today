from django.db import models


class Dish(models.Model):
    name = models.CharField(max_length=200, unique=True)
    main = models.BooleanField()
    url = models.CharField(max_length=300, null=True)
    categories = models.ManyToManyField('Category', through='DishCategory')
    additives = models.ManyToManyField('Additive', through='DishAdditive')
    allergies = models.ManyToManyField('Allergy', through='DishAllergy')
    mensen = models.ManyToManyField('Mensa', through='DishPlan')
    users = models.ManyToManyField('users.User', through='UserDishRating')
    ext_ratings = models.ManyToManyField(
        "Mensa", related_name="dish_ext_ratings", through="ExtDishRating")

    class Meta:
        verbose_name = 'Dish'
        verbose_name_plural = 'Dishes'


class Category(models.Model):
    name = models.CharField(max_length=40, unique=True)
    dishes = models.ManyToManyField('Dish', through='DishCategory')
    users = models.ManyToManyField('users.User', through='UserCategory')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Allergy(models.Model):
    name = models.CharField(max_length=40, unique=True)
    allergies = models.ManyToManyField('Dish', through='DishAllergy')
    users = models.ManyToManyField('users.User', through='UserAllergy')

    class Meta:
        verbose_name = 'Allergy'
        verbose_name_plural = 'Allergies'


class Additive(models.Model):
    name = models.CharField(max_length=40, unique=True)
    additives = models.ManyToManyField('Dish', through='DishAdditive')

    class Meta:
        verbose_name = 'Additive'
        verbose_name_plural = 'Additives'


class Mensa(models.Model):
    name_id = models.CharField(max_length=70, unique=True)
    name = models.CharField(max_length=70)
    street = models.CharField(max_length=100)
    houseNumber = models.CharField(max_length=20)
    zipCode = models.IntegerField()
    city = models.CharField(max_length=50)
    startTime = models.TimeField()
    endTime = models.TimeField()
    dishes = models.ManyToManyField("Dish", through="DishPlan")
    ext_ratings = models.ManyToManyField(
        "Dish", related_name="mensa_ext_ratings", through="ExtDishRating")
    lat = models.DecimalField(max_digits=13, decimal_places=8, null=True)
    lon = models.DecimalField(max_digits=13, decimal_places=8, null=True)
    rooms = models.ManyToManyField(
        "courses.Room", through="courses.RoomMensaDistance")

    class Meta:
        verbose_name = 'Mensa'
        verbose_name_plural = 'Mensen'


class CardBalance(models.Model):
    balance = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, null=False)

    class Meta:
        unique_together = (('id', 'date'),)


class DishCategory(models.Model):
    class Meta:
        unique_together = (('dish', 'category'),)

    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class DishAllergy(models.Model):
    class Meta:
        unique_together = (('dish', 'allergy'),)

    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    allergy = models.ForeignKey(Allergy, on_delete=models.CASCADE)


class DishAdditive(models.Model):
    class Meta:
        unique_together = (('dish', 'additive'),)

    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    additive = models.ForeignKey(Additive, on_delete=models.CASCADE)


class UserCategory(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class UserAllergy(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    allergy = models.ForeignKey(Allergy, on_delete=models.CASCADE)


class DishPlan(models.Model):
    class Meta:
        unique_together = (('dish', 'mensa', 'date'),)

    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    mensa = models.ForeignKey(Mensa, on_delete=models.CASCADE)
    date = models.DateField()
    priceStudent = models.DecimalField(max_digits=4, decimal_places=2)
    priceEmployee = models.DecimalField(max_digits=4, decimal_places=2)


class ExtDishRating(models.Model):
    class Meta:
        unique_together = (('dish', 'mensa', 'date'),)

    mensa = models.ForeignKey(Mensa, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    date = models.DateField()
    rating_avg = models.DecimalField(max_digits=2, decimal_places=1)
    rating_count = models.IntegerField()


class UserDishRating(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    rating = models.FloatField()
