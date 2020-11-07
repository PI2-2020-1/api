import json
from django.http import HttpResponseRedirect
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core import serializers
from .serializers import CustomUserSerializer, ReadingSerializer
from .models import User, Plantation, Reading, Station, Parameter


class SignUpVerification(APIView):

    def get(self, request, cpf):
        user = get_object_or_404(User, cpf=cpf)
        
        if user.is_active:
            return Response(status=401)

        return Response(status=200)


class TelegramVerification(APIView):

    def get(self, request, telegram):
        user = get_object_or_404(User, telegram=telegram)
        return JsonResponse({'full_name': user.full_name})


class EmployeesList(APIView):

    def get(self, request, username):
        user = get_object_or_404(User, username=username)

        # if not user.is_responsible:
        #     return JsonResponse(data={'message': 'Not responsible'}, status=401)

        plantation = get_object_or_404(Plantation, responsible=user.pk)
        employees = plantation.employees.all()
        serializer = CustomUserSerializer(employees, many=True)

        return JsonResponse(serializer.data, safe=False)
    
    def post(self, request, username, format=None):
        str_args = request.body.decode('utf-8')
        data = json.loads(str_args)

        employee = User.objects.create_user(
            cpf=data['cpf'],
            is_active=False,
            is_responsible=False,
            username=data['cpf'],
            telegram=data['cpf']
        )

        user = get_object_or_404(User, username=username)
        plantation = get_object_or_404(Plantation, responsible=user.pk)
        plantation.employees.add(employee)

        return Response(status=200)


class LatestData(APIView):
    
    def get(self, request, station_pk):
        station = get_object_or_404(Station, pk=station_pk)

        latest = []

        parameters = Parameter.get_all_types()
        for p in parameters:
            readings = Reading.objects.filter(
                station=station_pk,
                parameter=p 
            ).order_by('-time')
            if readings:
                latest.append(readings[0])

        serializer = ReadingSerializer(latest, many=True)

        return JsonResponse(serializer.data, safe=False)

