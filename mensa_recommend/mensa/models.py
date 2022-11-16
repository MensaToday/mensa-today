from django.db import models


class Dish(models.Model):
    name = models.CharField(max_length=200)
    categories = models.ManyToManyField('Category', through='DishCategory')
    allergies = models.ManyToManyField('Allergy', through='DishAllergy')
    mensen = models.ManyToManyField('Mensa', through='DishPlan')

    class Meta:
        verbose_name = 'Dish'
        verbose_name_plural = 'Dishes'


class Category(models.Model):
    id = models.CharField(primary_key=True, max_length=10, unique=True)
    name = models.CharField(max_length=40)
    dishes = models.ManyToManyField('Dish', through='DishCategory')
    users = models.ManyToManyField('users.User', through='UserCategory')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Allergy(models.Model):
    id = models.CharField(primary_key=True, max_length=10, unique=True)
    name = models.CharField(max_length=40)
    allergies = models.ManyToManyField('Dish', through='DishAllergy')
    users = models.ManyToManyField('users.User', through='UserAllergy')

    class Meta:
        verbose_name = 'Allergy'
        verbose_name_plural = 'Allergies'


class Additive(models.Model):
    id = models.CharField(primary_key=True, max_length=10, unique=True)
    name = models.CharField(max_length=40)
    additives = models.ManyToManyField('Dish', through='DishAdditive')

    class Meta:
        verbose_name = 'Additive'
        verbose_name_plural = 'Additives'


class Mensa(models.Model):
    name = models.CharField(max_length=70)
    street = models.CharField(max_length=100)
    housenumer = models.IntegerField()
    startTime = models.TimeField()
    endtime = models.TimeField()
    dishes = models.ManyToManyField("Dish", through="DishPlan")

    class Meta:
        verbose_name = 'Mensa'
        verbose_name_plural = 'Mensen'


class CardBalance(models.Model):
    balance = models.DecimalField(max_digits=2, decimal_places=2)
    date = models.DateField()
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)


class DishCategory(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class DishAllergy(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    allergy = models.ForeignKey(Allergy, on_delete=models.CASCADE)


class DishAdditive(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    additive = models.ForeignKey(Additive, on_delete=models.CASCADE)


class UserCategory(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class UserAllergy(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    allergy = models.ForeignKey(Allergy, on_delete=models.CASCADE)


class DishPlan(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    mensa = models.ForeignKey(Mensa, on_delete=models.CASCADE)
    date = models.DateField()
    priceStudent = models.DecimalField(max_digits=2, decimal_places=2)
    priceEmployee = models.DecimalField(max_digits=2, decimal_places=2)
