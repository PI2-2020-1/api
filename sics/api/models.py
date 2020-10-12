from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=70)
    cpf = models.CharField(max_length=12, unique=True)
    telegram = models.CharField(max_length=30)

    def __str__(self):
        return self.full_name


class Sensor(models.Model):
    name = models.CharField(max_length=50)
    upper_limit = models.FloatField()
    lower_limit = models.FloatField()
    ideal_value = models.FloatField()