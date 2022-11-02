from django.db import models


class Phone(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    price = models.FloatField()
    image = models.URLField()
    release_date = models.DateField()
    lte_exists = models.BooleanField()
