from django.contrib import admin
from django.urls import path
from .views import current_user, UserList, TemperatureList, TemperatureDetail


urlpatterns = [
    path('current_user/', current_user),
    path('users/', UserList.as_view()),
    path('temperatures/', TemperatureList.as_view()),
    path('temperature/<int:pk>/', TemperatureDetail.as_view()),
]
