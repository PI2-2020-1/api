from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('temperatures/', views.TemperatureList.as_view()),
    path('temperature/<int:pk>/', views.TemperatureDetail.as_view()),
]
