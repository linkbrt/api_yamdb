from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, CreateConfirmCodeMixin, RetrieveTokenAPIView


router = DefaultRouter()
router.register('users', UserViewSet)
router.register('auth/email', CreateConfirmCodeMixin)
router.register('auth/token', RetrieveTokenAPIView)

urlpatterns = [
    path('', include(router.urls)),
]
