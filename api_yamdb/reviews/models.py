import datetime

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Genres(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг',
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return str(self.name)


class Categories(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг',
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return str(self.name)


class Titles(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
    )
    year = models.PositiveSmallIntegerField(
        # From 1 to current year.
        validators=(
            MinValueValidator(1),
            MaxValueValidator(datetime.date.today().year),
        ),
        verbose_name='Год выпуска',
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание',
    )
    genre = models.ManyToManyField(
        Genres,
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
        related_name='category',
    )
