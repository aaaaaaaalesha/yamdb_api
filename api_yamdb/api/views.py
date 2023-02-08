import random
import string

from django.conf import settings
from django.core import mail
from django.db import models
from rest_framework import (filters, mixins, permissions, status, views,
                            viewsets)
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt import tokens

from reviews.models import Category, Genre, Title, User

from .permissions import IsAdmin
from .serializers import (CategorySerializer, GenreSerializer,
                          RegistrationSerializer, TitleModifySerializer,
                          TitleSerializer, TokenSerializer, UserSerializer)


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes =
    pagination_class = LimitOffsetPagination


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes =
    pagination_class = LimitOffsetPagination


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    # permission_classes =
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleModifySerializer
        return TitleSerializer


@action(detail=False, methods=['get', 'post', 'patch', 'delete'])
class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        methods=('GET', 'PATCH',),
        permission_classes=(IsAuthenticated,),
        detail=False,
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
            )
            return Response(serializer.data)
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save(role=request.user.role)
        return Response(serializer.data)


class RegistrationView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    MAIL_SUBJECT = 'Код подтверждения для регистрации в YamDB'
    FROM_MAIL = 'yamdb@yandex.ru'
    MAIL_TEXT = string.Template((
        'Привет, $username!\n'
        'Нам пришёл запрос на регистрацию от Вас. Если это были не Вы,'
        ' игнорируйте это письмо!\n'
        'Ваш код подтверждения: $confirmation_code\n'
        'Для окончания регистрации Вам необходимо выполнить запрос:\n'
        '[POST] /auth/token/\n'
        '{\n'
        '  "username": "$username",\n'
        '  "confirmation_code": "$confirmation_code"\n'
        '}'
    ))

    @staticmethod
    def generate_confirmation_code() -> str:
        return ''.join(
            random.choices(
                population=string.ascii_uppercase + string.digits,
                k=settings.CONFIRMATION_CODE_SIZE,
            )
        )

    def post(self, request) -> Response:
        serializer = RegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        fields = {
            'email': request.data.get('email'),
            'username': request.data.get('username'),
            'confirmation_code': self.generate_confirmation_code(),
        }

        mail.send_mail(
            subject=self.MAIL_SUBJECT,
            message=self.MAIL_TEXT.safe_substitute(fields),
            from_email=self.FROM_MAIL,
            recipient_list=[fields['email'], ],
        )
        users = User.objects.filter(
            email=fields['email'],
            username=fields['username'],
        )

        if users.exists():
            users.update(confirmation_code=fields['confirmation_code'])
            return Response(
                serializer.validated_data,
                status=status.HTTP_200_OK,
            )

        is_same_email_username = User.objects.filter(
            models.Q(email=fields['email'])
            | models.Q(username=fields['username'])
        ).exists()
        if is_same_email_username:
            return Response(
                {'error': 'User with such params already exists'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        User.objects.create(
            email=fields['email'],
            username=fields['username'],
            confirmation_code=fields['confirmation_code'],
        )

        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK,
        )    


class TokenView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request) -> Response:
        serializer = TokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        fields = {
            'username': request.data.get('username'),
            'confirmation_code': request.data.get('confirmation_code'),
        }
        users = User.objects.filter(username=fields['username'], )

        if users.exists():
            user = users.first()
            if user.confirmation_code != fields['confirmation_code']:
                return Response(
                    {'confirmation_code': 'incorrect code'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return Response(
                {'token': str(tokens.AccessToken.for_user(user))},
                status=status.HTTP_200_OK,
            )

        return Response(
            {'error': 'User with such params not found'},
            status=status.HTTP_404_NOT_FOUND,
        )




