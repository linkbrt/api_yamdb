from django.urls import include, path
from rest_framework import routers

from .views import (CategoriesViewSet, CommentViewSet, GenresViewSet,
                    ReviewViewSet, TitlesViewSet)

v1_router = routers.DefaultRouter()
v1_router.register('categories/', CategoriesViewSet, basename='categories')
v1_router.register('genres/', GenresViewSet, basename='genres')
v1_router.register('titles/', TitlesViewSet, basename='titles')
router_v1 = routers.SimpleRouter()

route = r'v1/titles/(?P<title_id>\d+)/reviews'

router_v1.register(
    route, ReviewViewSet, base_name='review')
router_v1.register(
    route + r'/(?P<review_id>\d+)',
    ReviewViewSet, base_name='review')

router_v1.register(
    route + r'/(?P<review_id>\d+)/comments',
    CommentViewSet, base_name='comment')
router_v1.register(
    route + r'/(?P<review_id>\d+)/comments/(?P<comment_id>\d+)',
    CommentViewSet, base_name='comment')

urlpatterns = [
    path('v1/', include(v1_router.urls))
]

urlpatterns += router_v1.urls
