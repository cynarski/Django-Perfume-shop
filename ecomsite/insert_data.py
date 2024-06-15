import os
import django
import csv
from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecomsite.settings")
django.setup()

from perfumeshop.models import Perfume

csv_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'products.csv')


with open(csv_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        Perfume.objects.create(
            brand=row['Brand'],
            name=row['Name'],
            type=row['Type'],
            price=float(row['Price'].replace(',', '.').replace(' ', '')),
            image=row['Image']
        )

print("Data load succesfully")