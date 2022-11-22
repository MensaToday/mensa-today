# Generated by Django 4.1.3 on 2022-11-22 15:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=80)),
                ('seats', models.IntegerField(null=True)),
            ],
        ),
        migrations.RemoveConstraint(
            model_name='timeslot',
            name='unique appversion',
        ),
        migrations.AddField(
            model_name='course',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='timeslot',
            name='endDate',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='timeslot',
            name='startDate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='learnweb_abbr',
            field=models.CharField(max_length=50),
        ),
        migrations.AddConstraint(
            model_name='timeslot',
            constraint=models.UniqueConstraint(fields=('weekDay', 'startTime', 'endTime', 'rythm', 'startDate', 'endDate'), name='unique timeslot'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.room'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='timeslot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.timeslot'),
        ),
    ]
