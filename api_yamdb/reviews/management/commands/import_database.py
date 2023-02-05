import os

from django.core.management.base import BaseCommand
from django.conf import settings
from csv import DictReader


class ImportDatabaseFromCSVCommand(BaseCommand):
    help = 'Displays current time'
    DEFAULT_PATH = os.path.join(
        settings.BASE_DIR,
        'static',
        'data',
    )

    def __process_path(self, path: str) -> None:
        if not os.path.exists(path):
            self.stderr.write(
                f'Passed {path} does not exist'
            )
            return

        files = {}
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

    def import_csv(self, csv_file: str) -> None:
        pass  # TODO: implement import from csv

    def handle(self, *paths):
        if not paths:
            paths = [self.DEFAULT_PATH, ]

        for path in paths:
            self.__process_path(path)
