# from django.urls import path
from rest_framework import routers

from .views import CommentViewSet, ReviewViewSet

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

urlpatterns = []

urlpatterns += router_v1.urls
