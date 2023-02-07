from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, GenreViewSet, RegistrationView,
                    TitleViewSet, TokenView, UsersViewSet)

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register(
    'users',
    UsersViewSet,
    basename='users',
)
router_v1.register(
    'genres',
    GenreViewSet,
    basename='genres'
)
router_v1.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
router_v1.register(
    'titles',
    TitleViewSet,
    basename='titles'
)


urlpatterns = [
    path('v1/auth/signup/', RegistrationView.as_view()),
    path('v1/auth/token/', TokenView.as_view()),
    path('v1/', include(router_v1.urls)),
]
