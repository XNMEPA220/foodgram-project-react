import csv
import os

from django.core.management.base import BaseCommand

from foodgram.models import Ingredient
from backend.settings import BASE_DIR


class Command(BaseCommand):
    help = 'Загрузка ингредиентов в базу данных'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(BASE_DIR, 'data', 'ingredients.csv')
        print(f' Put: {file_path}')
        with open(
                file_path, encoding='utf-8'
        ) as file:
            reader = csv.reader(file)
            next(reader)
            ingredients = [
                Ingredient(
                    name=row[0],
                    measurement_unit=row[1],
                )
                for row in reader
            ]
            Ingredient.objects.bulk_create(ingredients)
        print('Ингредиенты в базу данных загружены')
        print(f'{len(ingredients)} ингредиентов загружены')
