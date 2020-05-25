from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from sics.api.models import Temperature

class TemperatureSerializer(serializers.Serializer):
    value = serializers.FloatField()

    def create(self, validated_data):
        """
        Create and return a new `Temperature` instance, given the validated data.
        """
        return Temperature.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Temperature` instance, given the validated data.
        """
        instance.value = validated_data.get('value', instance.value)
        instance.save()
        return instance
