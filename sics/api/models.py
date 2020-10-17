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