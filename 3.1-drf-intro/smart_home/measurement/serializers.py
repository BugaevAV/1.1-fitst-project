from rest_framework import serializers

from measurement.models import Measurement, Sensor


class MeasurementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['temperature', 'created_at', 'image']


class SensorDetailSerializer(serializers.ModelSerializer):
    measurement_set = MeasurementsSerializer(many=True, read_only=True)

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'measurement_set']


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description']


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['id', 'temperature', 'created_at', 'sensor']
