<<<<<<< HEAD
from django.urls import path, include 
from rest_framework import routers 
from .views import CategoriesViewSet, GenresViewSet, TitlesViewSet
from rest_framework_simplejwt.views import ( 
        TokenObtainPairView, 
        TokenRefreshView, 
    ) 
 
v1_router = routers.DefaultRouter() 
v1_router.register('categories', CategoriesViewSet, basename='categories')
v1_router.register('genres', GenresViewSet, basename='genres')
v1_router.register('titles', TitlesViewSet, basename='titles')
 
urlpatterns = [ 
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('v1/', include(v1_router.urls)) 
    ]
=======
from django.urls import include, path
from rest_framework import routers

from .views import (CategoriesViewSet, CommentViewSet, GenresViewSet,
                    ReviewViewSet, TitlesViewSet)


v1_router = routers.DefaultRouter()
v1_router.register('categories', CategoriesViewSet, basename='categories')
v1_router.register('genres', GenresViewSet, basename='genres')
v1_router.register('titles', TitlesViewSet, basename='titles')

route = r'v1/titles/(?P<title_id>\d+)/reviews'

v1_router.register(
    route, ReviewViewSet, basename='review')
v1_router.register(
    route + r'/(?P<review_id>\d+)',
    ReviewViewSet, basename='review')
v1_router.register(
    route + r'/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment')
v1_router.register(
    route + r'/(?P<review_id>\d+)/comments/(?P<comment_id>\d+)',
    CommentViewSet, basename='comment')

urlpatterns = [
    path('v1/', include(v1_router.urls))
]
>>>>>>> develop
