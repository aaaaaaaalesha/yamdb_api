from rest_framework import mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination


from reviews.models import (
    Genres,
    Categories,
    Titles,
)

from .serializers import (
    GenreSerializer,
    CategorySerializer,
    TitleModifySerializer,
    TitleSerializer,
)


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer
    # permission_classes =
    pagination_class = LimitOffsetPagination


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    # permission_classes =
    pagination_class = LimitOffsetPagination


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    # permission_classes =
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleModifySerializer
        return TitleSerializer
