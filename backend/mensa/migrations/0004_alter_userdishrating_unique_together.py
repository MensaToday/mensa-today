# Generated by Django 4.1.3 on 2023-01-20 16:03

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mensa', '0003_alter_usersideselection_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userdishrating',
            unique_together={('user', 'dish')},
        ),
    ]