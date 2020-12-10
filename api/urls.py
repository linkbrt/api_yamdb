from django.urls import include, path
from rest_framework import routers

from .views import CategoriesViewSet, GenresViewSet, TitlesViewSet

v1_router = routers.DefaultRouter()
v1_router.register('categories/', CategoriesViewSet, basename='categories')
v1_router.register('genres/', GenresViewSet, basename='genres')
v1_router.register('titles/', TitlesViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(v1_router.urls))
]
