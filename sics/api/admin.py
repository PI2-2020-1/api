from django.contrib import admin
from .models import User, Plantation, Parameter, Reading, Station
# Register your models here.
admin.site.register(User)
admin.site.register(Plantation)
admin.site.register(Parameter)
admin.site.register(Reading)
admin.site.register(Station)