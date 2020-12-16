from django.urls import include, path
from rest_framework import routers

from .views import (CategoriesViewSet, CommentViewSet, GenresViewSet,
                    ReviewViewSet, TitlesViewSet, UserViewSet, register_user,
                    retrieve_token)

v1_router = routers.DefaultRouter()
v1_router.register('categories', CategoriesViewSet, basename='categories')
v1_router.register('genres', GenresViewSet, basename='genres')
v1_router.register('titles', TitlesViewSet, basename='titles')

v1_router.register('users', UserViewSet)

route = r'titles/(?P<title_id>\d+)/reviews'

v1_router.register(
    route + r'/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')
v1_router.register(
    route + r'/(?P<review_id>\d+)/comments/(?P<comment_id>\d+)',
    CommentViewSet, basename='comments')

v1_router.register(
    route, ReviewViewSet, basename='review')
v1_router.register(
    route + r'/(?P<review_id>\d+)',
    ReviewViewSet, basename='review')


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/email/', register_user),
    path('v1/auth/token/', retrieve_token),
]
