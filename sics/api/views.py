from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from sics.api.models import Sensor
from sics.api.serializers import SensorSerializer
from django.shortcuts import get_object_or_404
from .models import User
from django.http import JsonResponse


class SensorList(generics.ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class SignUpVerification(APIView):

    def get(self, request, cpf):
        user = get_object_or_404(User, cpf=cpf)
        return Response(status=200)


class TelegramVerification(APIView):

    def get(self, request, telegram):
        user = get_object_or_404(User, telegram=telegram)
        return JsonResponse({'full_name': user.full_name})