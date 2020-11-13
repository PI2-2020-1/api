from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from allauth.account import app_settings as allauth_settings
from allauth.utils import (email_address_exists, get_username_max_length)
from allauth.account.adapter import get_adapter
from .models import User, Reading, Parameter, Plantation, Station
from django.db.models import Q


class CustomRegisterSerializer(RegisterSerializer):
    full_name = serializers.CharField(write_only=True, required=True, max_length=70)
    cpf = serializers.CharField(write_only=True, required=True, max_length=12)
    telegram = serializers.CharField(write_only=True, required=True, max_length=30)
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    "A user is already registered with this e-mail address.")
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("The two password fields didn't match.")
        return data

    def get_cleaned_data(self):
        return {
            'full_name': self.validated_data.get('full_name', ''),
            'cpf': self.validated_data.get('cpf', ''),
            'telegram': self.validated_data.get('telegram', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', '')
        }

    def save(self, request):
        adapter = get_adapter()
        self.cleaned_data = self.get_cleaned_data()
        user = User.objects.get(cpf=self.cleaned_data.get('cpf'))
        user = adapter.save_user(request, user, self, commit=False)
        user.full_name = self.cleaned_data.get('full_name')
        user.telegram = self.cleaned_data.get('telegram')
        user.is_active = True
        user.save()
        return user


class CustomEmployeeSerializer(serializers.ModelSerializer):  
    class Meta: 
        model = User 
        fields = ('full_name', 'cpf', 'is_active', 'email')


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'


class PlantationSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    stations = serializers.SerializerMethodField()

    class Meta:
        model = Plantation
        fields = ('name', 'stations')

    def get_name(self, instance):
        return instance.farm + " - " + instance.name
    
    def get_stations(self, instance):
        stations = Station.objects.filter(plantation=instance)
        return StationSerializer(stations, many=True).data


class CustomUserSerializer(serializers.ModelSerializer):  
    plantations = serializers.SerializerMethodField()
    is_responsible = serializers.SerializerMethodField()

    class Meta: 
        model = User 
        fields = ('full_name', 'cpf', 'email', 'username', 'telegram', 'is_responsible', 'plantations')
    
    def get_plantations(self, instance):
        if instance.is_responsible():   
            plantantions = Plantation.objects.filter(responsible=instance)
        else:
            plantantions = Plantation.objects.filter(employees=instance)
        return PlantationSerializer(plantantions, many=True).data
    
    def get_is_responsible(self, instance):
        return instance.is_responsible()


class ReadingSerializer(serializers.ModelSerializer):
    parameter = serializers.SerializerMethodField()

    class Meta:
        model = Reading 
        fields = '__all__'
    
    def get_parameter(self, instance):
        return instance.parameter.parameter_type


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ('__all__') 


class CustomReadingSerializer(serializers.ModelSerializer):
    parameters = serializers.SerializerMethodField()

    class Meta:
        model = Reading 
        fields = ('value', 'time', 'parameters')

    def get_parameters(self, instance):
        parameters = Parameter.objects.filter(id=instance.parameter.id)
        return CustomParameterSerializer(parameters, many=True).data


class CustomParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ('parameter_type', 'min_value', 'max_value') 



class CustomStationSerializer(serializers.ModelSerializer):
    readings = serializers.SerializerMethodField()

    class Meta:
        model = Station
        fields = ('number', 'readings')


    def get_readings(self, instance):
        readings = Reading.objects.filter(station=instance)
        return CustomReadingSerializer(readings, many=True).data


class CustomPlantationSerializer(serializers.ModelSerializer):  
    users = serializers.SerializerMethodField()
    parameters = serializers.SerializerMethodField()


    class Meta: 
        model = Plantation 
        fields = ('farm', 'name', 'users', 'parameters')
    
    def get_users(self, instance):
        users = User.objects.filter(id=instance.responsible.id)
        return CustomUserPlantationSerializer(users, many=True).data

    def get_parameters(self, instance):
        parameters = Parameter.objects.filter(id=instance.parameter.id)
        return CustomParameterSerializer(parameters, many=True).data


class CustomUserPlantationSerializer(serializers.ModelSerializer):  
    plantations = serializers.SerializerMethodField()
    is_responsible = serializers.SerializerMethodField()

    class Meta: 
        model = User 
        fields = ('full_name', 'cpf', 'email', 'username', 'telegram', 'is_responsible', 'plantations')
    
    def get_plantations(self, instance):
        if instance.is_responsible():   
            plantantions = Plantation.objects.filter(responsible=instance)
        else:
            plantantions = Plantation.objects.filter(employees=instance)
        return CustomPlantationUserSerializer(plantantions, many=True).data
    
    def get_is_responsible(self, instance):
        return instance.is_responsible()


class CustomPlantationUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    stations = serializers.SerializerMethodField()

    class Meta:
        model = Plantation
        fields = ('name', 'stations')

    def get_name(self, instance):
        return instance.farm + " - " + instance.name
    
    def get_stations(self, instance):
        stations = Station.objects.filter(plantation=instance)
        return CustomStationSerializer(stations, many=True).data