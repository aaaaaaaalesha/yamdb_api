from rest_framework import serializers
from django.db import models

from reviews.models import (
    Genre,
    Category,
    Title,
)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'name',
            'slug',
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
        )


class TitleModifySerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        many=True,
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
    )

    class Meta:
        model = Title
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
        model = Title
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
