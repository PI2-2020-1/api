from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('sensors/', views.SensorList.as_view()),
    path('signup/verification/<cpf>', views.SignUpVerification.as_view()),
    path('telegram/verification/<telegram>', views.TelegramVerification.as_view())
]
