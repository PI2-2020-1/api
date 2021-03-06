import json
from django.http import HttpResponseRedirect
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core import serializers
from .serializers import CustomPlantationSerializer, CustomUserSerializer, CustomEmployeeSerializer, ReadingSerializer, StationSerializer, ParameterSerializer, CustomReadingSerializer
from .models import User, Plantation, Reading, Station, Parameter
from .util import send_alerts


class SignUpVerification(APIView):

    def get(self, request, cpf):
        user = get_object_or_404(User, cpf=cpf)

        if user.is_active:
            return Response(status=401)

        return Response(status=200)


class Profile(APIView):

    def post(self, request, username):
        user = get_object_or_404(User, username=username)

        str_args = request.body.decode('utf-8')
        data = json.loads(str_args)

        user.email = data['email']
        user.telegram = data['telegram']
        user.full_name = data['full_name']
        user.save()

        serializer = CustomUserSerializer(user)

        return JsonResponse(serializer.data, safe=False)

    def get(self, request, username):
        user = get_object_or_404(User, username=username)

        serializer = CustomUserSerializer(user)

        return JsonResponse(serializer.data, safe=False)


class TelegramVerification(APIView):

    def get(self, request, telegram, chat_id):
        user = get_object_or_404(User, telegram=telegram)
        user.chat_id = chat_id
        user.save()
        serializer = CustomUserSerializer(user)

        return JsonResponse(serializer.data, safe=False)


class EmployeesList(APIView):

    def get(self, request, username):
        user = get_object_or_404(User, username=username)

        # if not user.is_responsible:
        #     return JsonResponse(data={'message': 'Not responsible'}, status=401)

        plantation = get_object_or_404(Plantation, responsible=user.pk)
        employees = plantation.employees.all()
        serializer = CustomEmployeeSerializer(employees, many=True)

        return JsonResponse(serializer.data, safe=False)

    def post(self, request, username, format=None):
        str_args = request.body.decode('utf-8')
        data = json.loads(str_args)

        employee = User.objects.create_user(
            cpf=data['cpf'],
            is_active=False,
            username=data['cpf'],
            telegram=data['cpf']
        )

        user = get_object_or_404(User, username=username)
        plantation = get_object_or_404(Plantation, responsible=user.pk)
        plantation.employees.add(employee)

        return Response(status=200)

    def delete(self, request, username, format=None):
        user = get_object_or_404(User, username=username)

        plantation = get_object_or_404(Plantation, responsible=user.pk)

        str_args = request.body.decode('utf-8')
        data = json.loads(str_args)

        employee = get_object_or_404(User, cpf=data['cpf'])
        employee.delete()

        return Response(status=200)


class LatestData(APIView):

    def get(self, request, station_pk):
        station = get_object_or_404(Station, pk=station_pk)

        latest = []

        parameters = Parameter.get_all_types()
        for p in parameters:
            readings = Reading.objects.filter(
                station=station_pk,
                parameter__parameter_type=p
            ).order_by('-time')
            if readings:
                latest.append(readings[0])

        serializer = ReadingSerializer(latest, many=True)

        return JsonResponse(serializer.data, safe=False)

    def post(self, request, station_pk):
        str_args = request.body.decode('utf-8')
        data = json.loads(str_args)
        alerts = []

        for obj in data:
            parameter = get_object_or_404(
                Parameter, parameter_type=obj['parameter'])
            reading = Reading.objects.create(
                parameter=parameter,
                value=obj["value"],
                station=get_object_or_404(Station, pk=station_pk)
            )

            if not parameter.min_value <= obj['value'] <= parameter.max_value:
                alerts.append(reading)
        
        send_alerts(alerts)

        return Response(status=200)


class Report(APIView):

    def post(self, request):
        str_args = request.body.decode('utf-8')
        data = json.loads(str_args)

        report_list = []

        for p in data['parameter_list']:

            readings = Reading.objects.filter(
                time__range=[data['start'], data['end']],
                station__in=data['station_pk_list'],
                parameter__parameter_type=p
            ).order_by('-time')

            report_list.append(
                ReadingSerializer(readings, many=True).data
            )

        return JsonResponse(report_list, safe=False)


class ListStations(APIView):

    def get(self, request, plantation_pk):
        plantation = get_object_or_404(Plantation, pk=plantation_pk)

        stations = Station.objects.filter(plantation=plantation_pk)

        serializer = StationSerializer(stations, many=True)

        return JsonResponse(serializer.data, safe=False)

    # def post(self, request, plantation_pk):
    #     str_args = request.body.decode('utf-8')
    #     data = json.loads(str_args)

    #     for obj in data:
    #         station = Station.objects.create(
    #             number=obj["number"],
    #             plantation = get_object_or_404(Plantation, pk=plantation_pk)
    #         )

    #     return Response(status=200)


class ListUpdateParameter(APIView):

    # def get_object(self, pk):
    #     try:
    #         return Parameter.objects.get(pk=pk)
    #     except Parameter.DoesNotExist:
    #         raise Http404

    # def get(self, request, pk):
    #     parameter = get_object_or_404(Parameter, pk=pk)
    #     serializer = ParameterSerializer(parameter)

    #     return JsonResponse(serializer.data, safe=False)

    def post(self, request, station_pk):
        str_args = request.body.decode('utf-8')
        data = json.loads(str_args)
   
        plantation = get_object_or_404(Station, pk=station_pk).plantation
        parameter = Parameter.objects.filter(
            plantation=plantation, parameter_type=data['parameter_type']).first()

        if not parameter:
            Parameter.objects.create(
                parameter_type=data['parameter_type'],
                min_value=data['min_value'],
                max_value=data['max_value'],
                plantation=plantation
            )
        else:
            p = parameter
            p.parameter_type = data['parameter_type']
            p.min_value = min_value = data['min_value']
            p.max_value = data['max_value']
            p.save()

        return Response(status=200)


class Parameters(APIView):

    def get(self, request, plantation_pk):
        plantation = get_object_or_404(Plantation, pk=plantation_pk)

        parameter = Parameter.objects.filter(plantation=plantation_pk)

        serializer = ParameterSerializer(parameter, many=True)

        return JsonResponse(serializer.data, safe=False)

    def post(self, request, plantation_pk):
        str_args = request.body.decode('utf-8')
        data = json.loads(str_args)

        parameters = []

        for obj in data:
            if obj['id'] == "":
                p = Parameter.objects.create(
                    parameter_type=obj['parameter_type'],
                    min_value=obj['min_value'],
                    max_value=obj['max_value'],
                    plantation__pk=obj['plantation']
                )
            else:
                p = get_object_or_404(
                    Parameter, plantation__pk=plantation_pk, parameter_type=obj['parameter_type'])
                p.parameter_type = obj['parameter_type']
                p.min_value = min_value = obj['min_value']
                p.max_value = obj['max_value']
                p.save()

            parameters.append(p)

            serializer = ParameterSerializer(parameters, many=True)

        return JsonResponse(serializer.data, safe=False)


class ListReading(APIView):

    def get(self, request, station_pk):

        station = get_object_or_404(Station, pk=station_pk)

        latest = []

        parameters = Parameter.get_all_types()
        for p in parameters:
            readings = Reading.objects.filter(
                station=station_pk,
                parameter__parameter_type=p
            ).order_by('-time')
            if readings:
                latest.append(readings[0])

        serializer = CustomReadingSerializer(latest, many=True)

        return JsonResponse(serializer.data, safe=False)


class Plantations(APIView):

    def get(self, request, plantation_pk):
        plantation = get_object_or_404(Plantation, pk=plantation_pk)

        serializer = CustomPlantationSerializer(plantation)

        return JsonResponse(serializer.data, safe=False)
