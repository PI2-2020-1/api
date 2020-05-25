from django.contrib import admin
from django.urls import path
from .views import TemperatureList, TemperatureDetail


urlpatterns = [
    path('temperatures/', TemperatureList.as_view()),
    path('temperature/<int:pk>/', TemperatureDetail.as_view()),
]
