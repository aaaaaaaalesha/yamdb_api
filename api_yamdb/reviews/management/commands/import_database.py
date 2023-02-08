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


def _add_genres(row):
    Genre.objects.get_or_create(
        id=row['id'],
        name=row['name'],
        slug=row['slug'],
    )


def _add_categories(row):
    Category.objects.get_or_create(
        id=row['id'],
        name=row['name'],
        slug=row['slug'],
    )


def _add_titles(row):
    Title.objects.get_or_create(
        id=row['id'],
        name=row['name'],
        year=row['year'],
        category=row['category_id'],
    )


def _add_users(row):
    User.objects.get_or_create(
        id=row['id'],
        username=row['username'],
        email=row['email'],
        role=row['role'],
        bio=row['bio'],
        first_name=row['first_name'],
        last_name=row['last_name'],
    )


def _add_reviews(row):
    title, _ = Title.objects.get_or_create(id=row['title_id'])
    Review.objects.get_or_create(
        id=row['id'],
        title=title,
        text=row['text'],
        author=row['author'],
        score=row['score'],
        pub_date=row['pub_date']
    )


def _add_comments(row):
    review, _ = Review.objects.get_or_create(id=row['review_id'])
    Comment.objects.get_or_create(
        id=row['id'],
        author=row['author'],
        review=review,
        text=row['text'],
        pub_date=row['pub_date'],
    )


class Command(BaseCommand):
    """ImportDatabaseFromCSVCommand"""
    help = 'Imports database from csv by passed path.'
    DEFAULT_PATH = os.path.join(
        settings.BASE_DIR,
        'static',
        'data',
    )

    CSV_MODELS = {
        'genre.csv': _add_genres,
        'category.csv': _add_categories,
        'titles.csv': _add_titles,
        'users.csv': _add_users,
        'review.csv': _add_reviews,
        'comments.csv': _add_comments,
    }

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
        basename = os.path.basename(csv_file_path)
        procedure = self.CSV_MODELS.get(basename)
        if procedure is None:
            self.stderr(
                f'Basename of {csv_file_path} not '
                f'matches any of {self.CSV_MODELS.keys()}'
            )
            return

        with open(csv_file_path, encoding='utf-8', mode='r') as csv_file:
            dict_reader = csv.DictReader(csv_file)
            for row in dict_reader:
                procedure(row)

    def handle(self, *paths, **options):
        if not paths:
            paths = [self.DEFAULT_PATH, ]

        for path in paths:
            self.__process_path(path)
