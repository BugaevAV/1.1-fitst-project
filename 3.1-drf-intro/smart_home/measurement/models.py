from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.PROTECT)
    temperature = models.DecimalField(max_digits=3, decimal_places=1)
    created_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/', null=True)
