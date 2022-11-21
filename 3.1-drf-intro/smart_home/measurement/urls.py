from django.urls import path

from measurement.views import SensorView, SensorsListView, MeasurementsView

urlpatterns = [
    path('sensors/', SensorsListView.as_view()),
    path('sensors/<pk>/', SensorView.as_view()),
    path('measurements/', MeasurementsView.as_view()),
]
