from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from rest_framework import decorators, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Confirm, Profile
from .permissions import IsAdminOrDeny
from .serializers import (CreateConfirmCodeSerializer, ProfileSerializer,
                          RetrieveTokenSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'username'
    permission_classes = (IsAuthenticated, IsAdminOrDeny, )


@decorators.api_view(('GET', 'PATCH', ), )
@decorators.permission_classes([IsAuthenticated, ])
def api_get_profile(request):
    if request.method == 'GET':
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data, status=200)
    elif request.method == 'PATCH':
        serializer = ProfileSerializer(instance=request.user,
                                       data=request.data,
                                       context=request,
                                       partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=200)
        return Response(serializer.errors, status=400)


class CreateConfirmCodeMixin(viewsets.ViewSet, CreateAPIView):
    queryset = Confirm.objects.all()
    serializer_class = CreateConfirmCodeSerializer
    permission_classes = (AllowAny, )

    def perform_create(self, serializer):
        code = get_random_string(10)
        serializer.save(confirmation_code=code)
        send_mail(
            'Confirmation code',
            code,
            'yamdb@api.com',
            [serializer.data['email'], ])


class RetrieveTokenAPIView(viewsets.ViewSet, CreateAPIView):
    queryset = Confirm.objects.all()
    serializer_class = RetrieveTokenSerializer
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'token': str(token)}, status=201, headers=headers)

    def perform_create(self, serializer):
        user = Profile.objects.get_or_create(
            email=serializer.data['email']
        )
        get_object_or_404(Confirm, **serializer.data).delete()
        return RefreshToken.for_user(user[0]).access_token
