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