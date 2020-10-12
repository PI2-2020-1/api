from django.contrib import admin
from django.urls import path
from .views import SensorList, SignUpVerification


urlpatterns = [
    path('sensors/', SensorList.as_view()),
    path('signup/verification/<cpf>', SignUpVerification.as_view())
]
