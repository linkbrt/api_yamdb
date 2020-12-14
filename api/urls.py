from django.urls import include, path
from rest_framework import routers

from .views import (CategoriesViewSet, CommentViewSet, CreateConfirmCodeMixin,
                    GenresViewSet, RetrieveTokenAPIView, ReviewViewSet,
                    TitlesViewSet, UserViewSet)

v1_router = routers.DefaultRouter()
v1_router.register('categories', CategoriesViewSet, basename='categories')
v1_router.register('genres', GenresViewSet, basename='genres')
v1_router.register('titles', TitlesViewSet, basename='titles')

v1_router.register('users', UserViewSet)
v1_router.register('auth/email', CreateConfirmCodeMixin)
v1_router.register('auth/token', RetrieveTokenAPIView)

v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')

v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='review')

urlpatterns = [
    path('v1/', include(v1_router.urls))
]
