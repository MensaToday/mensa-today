# Generated by Django 4.1.3 on 2023-02-01 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='learnweb_abbr',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='room',
            name='address',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]