from django.db import models


class Course(models.Model):
    publishId = models.BigIntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    learnweb_abbr = models.CharField(max_length=50)
    users = models.ManyToManyField("users.User", through='UserCourse')


class Timeslot(models.Model):
    weekDay = models.CharField(max_length=50)
    startTime = models.TimeField()
    endTime = models.TimeField()
    startDate = models.DateField(auto_now=False, auto_now_add=False, null=True)
    endDate = models.DateField(auto_now=False, auto_now_add=False, null=True)
    rythm = models.CharField(max_length=10)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['weekDay', 'startTime', 'endTime', 'rythm', 'startDate', 'endDate'], name='unique timeslot')
        ]


class Room(models.Model):
    id = models.BigIntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=80)
    seats = models.IntegerField(null=True)
    lon = models.DecimalField(max_digits=13, decimal_places=8, null=True)
    lat = models.DecimalField(max_digits=13, decimal_places=8, null=True)
    mensen = models.ManyToManyField(
        'mensa.Mensa', through='RoomMensaDistance')


class Reservation(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(Timeslot, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['course', 'timeslot', 'room'], name='unique reservation')
        ]


class RoomMensaDistance(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    mensa = models.ForeignKey('mensa.Mensa', on_delete=models.CASCADE)
    distance = models.FloatField()


class UserCourse(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    crawl_date = models.DateTimeField(auto_now_add=True)
