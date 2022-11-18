# Generated by Django 4.1.3 on 2022-11-12 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mensa', '0002_usercategory_userallergy_allergy_users_and_more'),
        ('users', '0002_rename_las_name_user_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='allergies',
            field=models.ManyToManyField(through='mensa.UserAllergy', to='mensa.allergy'),
        ),
        migrations.AddField(
            model_name='user',
            name='categories',
            field=models.ManyToManyField(through='mensa.UserCategory', to='mensa.category'),
        ),
    ]