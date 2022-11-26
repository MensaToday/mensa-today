# Generated by Django 4.1.3 on 2022-11-12 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('publishId', models.BigIntegerField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('learnweb_abbr', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Timeslot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekDay', models.CharField(max_length=50)),
                ('startTime', models.TimeField()),
                ('endTime', models.TimeField()),
                ('rythm', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddConstraint(
            model_name='timeslot',
            constraint=models.UniqueConstraint(fields=('weekDay', 'startTime', 'endTime', 'rythm'), name='unique appversion'),
        ),
    ]