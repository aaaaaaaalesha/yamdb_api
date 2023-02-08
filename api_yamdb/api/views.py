import random
import string

from django.core import mail
from django.db import models
from django.shortcuts import get_object_or_404

from rest_framework import (
    mixins,
    viewsets,
    views,
    permissions,
    filters,
    status,
)
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt import tokens

from django_filters.rest_framework import DjangoFilterBackend

from .filters import TitleFilter

from reviews.models import (
    Genre,
    Category,
    Title,
    User,
    Review,
    Comment,
)

from .permissions import (
    IsAuthorOrStaffOrReadOnly,
    IsAdmin,
    IsAdminOrReadOnly,
)

from .serializers import (
    GenreSerializer,
    CategorySerializer,
    TitleModifySerializer,
    TitleReadSerializer,
    ReviewSerializer,
    CommentSerializer,
    UserSerializer,
    RegistrationSerializer,
    GetJWTokenSerializer,
)

# To not allow http-PUT method.
COMMON_METHODS = ('get', 'post', 'patch', 'delete')


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    # for delete /genres/{slug}/
    lookup_field = 'slug'


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    # for delete /categories/{slug}/
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    search_fields = ('genre',)
    http_method_names = COMMON_METHODS

    def get_queryset(self):
        return Title.objects.annotate(
            rating=models.Avg('reviews__score')
        )

    def get_serializer_class(self):
        if self.request.method not in permissions.SAFE_METHODS:
            return TitleModifySerializer
        return TitleReadSerializer


@action(detail=False, methods=COMMON_METHODS)
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrStaffOrReadOnly,
    )

    def get_queryset(self):
        title = Title.objects.get(id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def create(self, request, *args, **kwargs):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer = ReviewSerializer(data=request.data)

        if title.reviews.filter(author=self.request.user).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=self.request.user, title_id=title.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        review = get_object_or_404(Review, id=self.kwargs.get('pk'),
                                   title__id=self.kwargs.get('title_id'))

        user = self.request.user
        if user != review.author and not (user.is_admin or user.is_moderator):
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


@action(detail=False, methods=COMMON_METHODS)
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrStaffOrReadOnly,
    )

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id'),
        )
        return review.comments.all()

    def create(self, request, *args, **kwargs):
        review = get_object_or_404(
            Review,
            id=self.kwargs['review_id'],
            title__id=self.kwargs.get('title_id'),
        )
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=self.request.user, review_id=review.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        comment = get_object_or_404(
            Comment,
            id=self.kwargs.get('pk'),
            review__id=self.kwargs.get('review_id'),
        )

        user = self.request.user
        if user != comment.author and not (user.is_admin or user.is_moderator):
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = CommentSerializer(comment, data=request.data,
                                       partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    # for /users/{username}/
    lookup_field = 'username'

    http_method_names = COMMON_METHODS

    @action(
        methods=('GET', 'PATCH',),
        permission_classes=(IsAuthenticated,),
        detail=False,
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)

        # PATCH.
        serializer = UserSerializer(
            request.user, data=request.data, partial=True
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
    def __generate_confirmation_code() -> str:
        """
        Generates uppercase confirmation code with length
        User.CONFIRMATION_CODE_SIZE from uppercase alphanumeric alphabet.
        """
        return ''.join(
            random.choices(
                population=string.ascii_uppercase + string.digits,
                k=User.CONFIRMATION_CODE_SIZE,
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
            'confirmation_code': self.__generate_confirmation_code(),
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


class GetJWTokenView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request) -> Response:
        serializer = GetJWTokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
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
