from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from allauth.account import app_settings as allauth_settings
from allauth.utils import (email_address_exists, get_username_max_length)
from allauth.account.adapter import get_adapter
from .models import User, Reading, Parameter, Plantation, Station


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


class CustomUserSerializer(serializers.ModelSerializer):  
    class Meta: 
        model = User 
        fields = ('full_name', 'cpf', 'email', 'username', 'telegram', 'is_responsible')


class ReadingSerializer(serializers.ModelSerializer):
    parameter = serializers.SerializerMethodField()

    class Meta:
        model = Reading 
        fields = '__all__'
    
    def get_parameter(self, instance):
        return instance.parameter.parameter_type


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__' 


class ParameterSerialize(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = '__all__' 