from rest_framework import serializers
from django.db import models

from reviews.models import (
    Genres,
    Categories,
    Titles,
)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = (
            'name',
            'slug',
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = (
            'name',
            'slug',
        )


class TitleModifySerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all(),
        many=True,
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genres.objects.all(),
    )

    class Meta:
        model = Titles
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
        )


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField(method_name='get_mean_score')
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Titles
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )

    def get_mean_score(self, obj):
        """Calculates rating as mean scores value."""
        return obj.reviews.aggregate(
            models.Avg('score')
        ).get('score__avg')
