from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('signup/verification/<cpf>', views.SignUpVerification.as_view()),
    path('telegram/verification/<telegram>/<chat_id>', views.TelegramVerification.as_view()),
    path('employees/<username>', views.EmployeesList.as_view()),
    path('latest/<station_pk>', views.LatestData.as_view()),
    path('report', views.Report.as_view()),
    path('stations/<plantation_pk>', views.ListStations.as_view()),
    path('parameter/<plantation_pk>', views.ListUpdateParameter.as_view()),
]
