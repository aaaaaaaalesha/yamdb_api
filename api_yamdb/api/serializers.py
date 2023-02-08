from rest_framework import serializers
from django.core import validators

from reviews.models import (
    Genre,
    Category,
    Title,
    Review,
    Comment,
    User,
)

from .validators import me_username_validator


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


class TitleSerializer(serializers.ModelSerializer):
    # We don't need to store it in model.
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleModifySerializer(TitleSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False,
    )


class TitleReadSerializer(TitleSerializer):
    genre = GenreSerializer(
        many=True,
        read_only=True,
    )
    category = CategorySerializer(
        read_only=True,
    )


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


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = ('id', 'author', 'text', 'score', 'pub_date')


class RegistrationSerializer(serializers.Serializer):
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


class GetJWTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        validators=(
            validators.RegexValidator(r'^[\w.@+-]+\Z'),
            me_username_validator,
        )
    )
    confirmation_code = serializers.CharField(
        # For fixed length = CONFIRMATION_CODE_SIZE.
        validators=(validators.MinLengthValidator(
            User.CONFIRMATION_CODE_SIZE
        ),),
        max_length=User.CONFIRMATION_CODE_SIZE,
    )
