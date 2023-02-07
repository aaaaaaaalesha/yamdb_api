from django.conf import settings
from django.core import validators
from django.db import models
from rest_framework import serializers

from reviews.models import Category, Genre, Title, User

from .validators import me_username_validator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
    )
    username = serializers.CharField(
        max_length=150,
        validators=(
            validators.RegexValidator(r'^[\w.@+-]+\Z'),
            me_username_validator,
        )
    )


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        validators=(
            validators.RegexValidator(r'^[\w.@+-]+\Z'),
            me_username_validator,
        )
    )
    confirmation_code = serializers.CharField(
        validators=(validators.MinLengthValidator(
            settings.CONFIRMATION_CODE_SIZE
        ),),
        max_length=settings.CONFIRMATION_CODE_SIZE,
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
