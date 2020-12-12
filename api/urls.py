from django.urls import include, path
from rest_framework import routers

from .views import (CategoriesViewSet, CommentViewSet, GenresViewSet,
                    ReviewViewSet, TitlesViewSet)


v1_router = routers.DefaultRouter()
v1_router.register('categories', CategoriesViewSet, basename='categories')
v1_router.register('genres', GenresViewSet, basename='genres')
v1_router.register('titles', TitlesViewSet, basename='titles')

route = r'titles/(?P<title_id>\d+)/reviews'

v1_router.register(
    route, ReviewViewSet, basename='review')
v1_router.register(
    route + r'/(?P<review_id>\d+)',
    ReviewViewSet, basename='review_id')

v1_router.register(
    route + r'/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')
v1_router.register(
    route + r'/(?P<review_id>\d+)/comments/(?P<comment_id>\d+)',
    CommentViewSet, basename='comments_id')

urlpatterns = [
    path('v1/', include(v1_router.urls))
]
