from django.contrib import admin
from .models import User, Plantation, Parameter, Reading
# Register your models here.
admin.site.register(User)
admin.site.register(Plantation)
admin.site.register(Parameter)
admin.site.register(Reading)