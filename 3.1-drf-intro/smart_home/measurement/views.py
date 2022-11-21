from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from measurement.models import Sensor, Measurement
from measurement.serializers import SensorDetailSerializer, SensorSerializer, MeasurementSerializer


class SensorsListView(ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class SensorView(RetrieveUpdateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer


class MeasurementsView(ListCreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
