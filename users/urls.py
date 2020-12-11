from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CreateConfirmCodeMixin, RetrieveTokenAPIView, UserViewSet,
                    api_get_profile)

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('auth/email', CreateConfirmCodeMixin)
router.register('auth/token', RetrieveTokenAPIView)

urlpatterns = [
    path('users/me/', api_get_profile),
    path('', include(router.urls)),
]
