from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from sics.api.models import Sensor, User

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'upper_limit', 'ideal_value', 'lower_limit']