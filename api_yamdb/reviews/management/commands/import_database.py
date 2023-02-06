import os
import csv

from django.core.management.base import BaseCommand
from django.conf import settings

from ...models import (
    Genre,
    Category,
    Title,
    User,
    Review,
    Comment,
)


class Command(BaseCommand):
    """ImportDatabaseFromCSVCommand"""
    help = 'Imports database from csv by passed path.'
    DEFAULT_PATH = os.path.join(
        settings.BASE_DIR,
        'static',
        'data',
    )

    # CSV_MODELS = {
    #     'genre.csv': Genre,
    #     'category.csv': Category,
    #     'titles.csv': Title,
    #     'users.csv': User,
    #
    # }

    def __process_path(self, path: str) -> None:
        if not os.path.exists(path):
            self.stderr.write(
                f'Passed {path} does not exist'
            )
            return

        files = set()
        if os.path.isdir(path):
            files.update({
                os.path.join(path, p)
                for p in os.listdir(path)
                if p.endswith('.csv')
            })
        elif path.endswith('.csv'):
            files.update(path)
        else:
            self.stderr.write(
                f'Passed {path} not matches anything'
            )
            return

        for file in files:
            self.import_csv(file)

    def import_csv(self, csv_file_path: str) -> None:
        with open(csv_file_path, encoding='utf-8', mode='r') as csv_file:
            dict_reader = csv.DictReader(csv_file)
            # fields = dict_reader.fieldnames
            # print(dict_reader)
            # print(fields)

    def handle(self, *paths, **options):
        if not paths:
            paths = [self.DEFAULT_PATH, ]

        for path in paths:
            self.__process_path(path)
