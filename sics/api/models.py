from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=70)
    cpf = models.CharField(max_length=12, unique=True)
    telegram = models.CharField(max_length=30, unique=True)
    chat_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.full_name

    def is_responsible(self):
        return Plantation.objects.filter(responsible=self).exists()


class Plantation(models.Model):
    farm = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    responsible = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='responsible_plantation')
    employees = models.ManyToManyField(to=User, blank=True, related_name='employee_plantation')

    def get_all_users(self):
        users = []

        users.append(self.responsible)

        for u in self.employees.all():
            users.append(u)
        
        return users


class Station(models.Model):
    number = models.IntegerField()
    plantation = models.ForeignKey(Plantation, on_delete=models.DO_NOTHING)


class Parameter(models.Model):
    WIND = 0
    PRESSURE = 1
    AIR_TEMPERATURE = 2
    PH = 3
    SOIL_UMIDITY = 4
    AIR_UMIDITY = 5
    RAIN = 6

    parameter_type = models.IntegerField()
    min_value = models.FloatField()
    max_value = models.FloatField()
    plantation = models.ForeignKey(Plantation, on_delete=models.CASCADE)

    @staticmethod
    def get_all_types():
        return [Parameter.WIND, Parameter.PRESSURE, Parameter.AIR_TEMPERATURE, 
            Parameter.PH, Parameter.SOIL_UMIDITY, Parameter.AIR_UMIDITY, Parameter.RAIN]
    
    def get_parameter_name(self):
        if self.parameter_type == Parameter.WIND: return "Vento"
        if self.parameter_type  == Parameter.PRESSURE: return "Pressão Atmosférica"
        if self.parameter_type  == Parameter.AIR_TEMPERATURE: return "Temperatura do Ar"
        if self.parameter_type  == Parameter.PH: return "Ph"
        if self.parameter_type  == Parameter.SOIL_UMIDITY: return "Umidade do solo"
        if self.parameter_type  == Parameter.AIR_UMIDITY: return "Umidade do ar"
        if self.parameter_type  == Parameter.RAIN: return "Índice Pluviométrico"


class Reading(models.Model):
    parameter = models.ForeignKey(Parameter, on_delete=models.DO_NOTHING)
    value = models.FloatField()
    time = models.DateTimeField(auto_now=False, auto_now_add=True)
    station = models.ForeignKey(Station, on_delete=models.DO_NOTHING)


