import csv
from django.core.management.base import BaseCommand, CommandError

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загружает ингредиенты из csv-файла /data/ingredients.csv'

    def handle(self, *args, **options):

        print('Загрузка ингредиентов в базу ... ', end='')
        try:
            with open('./data/ingredients.csv') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    Ingredient(
                        name=row[0],
                        measurement_unit=row[1],
                    ).save()
                print('Done')
        except FileNotFoundError:
            raise CommandError('Файл с данными отсутствует')
        except (IndexError, AttributeError):
            raise CommandError('Ошибка входных данных')
        except PermissionError:
            raise CommandError('Ошибка доступа к файлу')
        except OSError:
            raise CommandError('Ошибка файловой системы')
