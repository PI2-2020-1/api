from django.http import HttpResponseRedirect
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core import serializers
from .serializers import CustomUserSerializer
from .models import User, Plantation


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

        if not user.is_responsible:
            return JsonResponse(data={'message': 'Not responsible'}, status=401)

        plantation = get_object_or_404(Plantation, responsible=user.pk)
        employees = plantation.employees.all()
        serializer = CustomUserSerializer(employees, many=True)

        return JsonResponse(serializer.data, safe=False)