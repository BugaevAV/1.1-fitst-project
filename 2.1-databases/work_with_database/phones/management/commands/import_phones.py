import csv
import re

from django.core.management.base import BaseCommand
from phones.models import Phone


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('csv', type=str, help='previously added csv')

    def handle(self, *args, **options):
        with open(options['csv'], 'r') as file:
            phones = list(csv.DictReader(file, delimiter=';'))
            for phone in phones:
                phone_info = Phone(name=phone['name'],
                                   slug=re.sub(r"\s", r"-", phone['name']),
                                   price=phone['price'], image=phone['image'],
                                   release_date=phone['release_date'],
                                   lte_exists=phone['lte_exists'])
                phone_info.save()
