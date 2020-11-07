from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=70)
    cpf = models.CharField(max_length=12, unique=True)
    telegram = models.CharField(max_length=30, unique=True)
    is_responsible = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name


class Plantation(models.Model):
    farm = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    responsible = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='responsible_plantation')
    employees = models.ManyToManyField(to=User, blank=True, related_name='employee_plantation')


class Station(models.Model):
    number = models.IntegerField()


class Parameter(models.Model):
    WIND = 0
    SOIL_TEMPERATURE = 1
    AIR_TEMPERATURE = 2
    PH = 3
    SOIL_UMIDITY = 4
    AIR_UMIDITY = 5
    RAIN = 6

    parameter_type = models.IntegerField()
    min_value = models.FloatField()
    max_value = models.FloatField()
    plantation = models.ForeignKey(Plantation, on_delete=models.CASCADE)


class Reading(models.Model):
    parameter = models.ForeignKey(Parameter, on_delete=models.DO_NOTHING)
    value = models.FloatField()
    time = models.DateTimeField(auto_now=False, auto_now_add=True)
    station = models.ForeignKey(Station, on_delete=models.DO_NOTHING)


