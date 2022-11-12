from django.db import models

class Course(models.Model):
    publishId = models.BigIntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    learnweb_abbr = models.CharField(max_length=20)
    
class Timeslot(models.Model):
    weekDay = models.CharField(max_length=50)
    startTime = models.TimeField()
    endTime = models.TimeField()
    rythm = models.CharField(max_length=10)
    
    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['weekDay', 'startTime', 'endTime', 'rythm'], name='unique timeslot')
        ]
    
