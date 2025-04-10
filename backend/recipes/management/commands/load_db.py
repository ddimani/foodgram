import json
import os

from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from foodgram_backend.settings import CORE_DIR
from recipes.models import Ingredient


class Command(BaseCommand):
    """Команда заполнение базы данных ингредиентов"""

    help = 'Загрузка данных для ингредиентов'


    def handle(self, *args, **options):
        try:
            with open(
                os.path.join(
                    CORE_DIR,
                    'data/ingredients.json'
                ),
                'r',
                encoding='utf-8'
            ) as data:
                data = json.load(data)
                for ingredient in data:
                    try:
                        Ingredient.objects.create(
                            name=ingredient['name'],
                            measurement_unit=ingredient['measurement_unit']
                        )

                    except IntegrityError:
                        pass
                self.stdout.write('Загрузка данных завершена!')
        except FileNotFoundError:
            raise CommandError('Файл ingredients.json не найден!')
