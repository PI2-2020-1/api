from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('signup/verification/<cpf>', views.SignUpVerification.as_view()),
    path('telegram/verification/<telegram>', views.TelegramVerification.as_view()),
    path('employees/<username>', views.EmployeesList.as_view()),
    path('latest/<station_pk>', views.LatestData.as_view()),
    path('report', views.Report.as_view()),
    path('station/<plantation_pk>', views.Station.as_view()),
    path('parameter', views.Parameter.as_view()),
]
