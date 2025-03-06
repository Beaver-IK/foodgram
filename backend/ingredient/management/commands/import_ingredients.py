from django.core.management.base import BaseCommand
import json
import csv
from foodgram.settings import BASE_DIR

from ingredient.models import Ingredient



class Command(BaseCommand):
    help = 'Импортирует ингредиенты из JSON файла'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Путь к CSV файлу')
    
    def handle(self, *args, **kwargs):
        file_path = BASE_DIR / kwargs['file_path']

        if not file_path.exists():
            self.stderr.write(f'Файл не найден: {file_path}')
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)

                for row in reader:
                    if len(row) != 2:
                        self.stderr.write(f'Неверный формат строки: {row}')
                        continue

                    name, measurement_unit = row

                    if not Ingredient.objects.filter(name=name).exists():
                        try:
                            ingredient = Ingredient(
                                name=name.strip(),
                                measurement_unit=measurement_unit.strip()
                            )
                            ingredient.save()
                            self.stdout.write(self.style.SUCCESS(
                                f'Добавлен ингредиент: {name}')
                            )
                        except Exception as e:
                            self.stderr.write(f'Ошибка при добавлении ингредиента {name}: {e}')
                    else:
                        self.stdout.write(
                            f'Ингредиент "{name}" уже существует '
                            'в базе данных.'
                        )
        except Exception as e:
            self.stderr.write(f'Произошла ошибка при чтении файла: {e}')

    """def handle(self, *args, **kwargs):
        file_path = BASE_DIR / kwargs['file_path']

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            for item in data:
                name = item.get('name')
                measurement_unit = item.get('measurement_unit')

                if not Ingredient.objects.filter(name=name).exists():
                    try:
                        ingredient = Ingredient(
                            name=name,
                            measurement_unit=measurement_unit
                        )
                        ingredient.save()
                        self.stdout.write(self.style.SUCCESS(f'Добавлен ингредиент: {name}'))
                    except Exception as e:
                        self.stderr.write(f'Ошибка при добавлении ингредиента {name}: {e}')
                else:
                    self.stdout.write(f'Ингредиент "{name}" уже существует в базе данных.')
        except FileNotFoundError:
            self.stderr.write(f'Файл не найден: {file_path}')
        except json.JSONDecodeError:
            self.stderr.write('Ошибка декодирования JSON файла.')"""