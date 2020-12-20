from django.core.mail import send_mail
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (decorators, filters, generics, mixins, permissions,
                            viewsets)
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsAdminOrReadOnly, IsOwnerOrStaffOrReadOnly

from .filters import TitleFilter
from .models import Category, Confirm, Genre, Profile, Review, Title
from .permissions import (IsAdminOrDeny, IsAdminOrReadOnly, IsOwnerOrReadOnly,
                          IsStaffOrReadOnly)
from .serializers import (CategorieSerializer, CommentSerializer,
                          CreateConfirmCodeSerializer, CreateTitleSerializer,
                          GenreSerializer, MyOwnProfileSerializer,
                          ProfileSerializer, RetrieveTokenSerializer,
                          ReviewSerializer, TitleSerializer)


class DefaultViewSet(
            viewsets.ModelViewSet,
            mixins.CreateModelMixin,
            mixins.DestroyModelMixin,
            mixins.ListModelMixin):
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)


class CategoriesViewSet(
        viewsets.ViewSet,
        generics.CreateAPIView,
        mixins.ListModelMixin,
        mixins.DestroyModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorieSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend, )
    search_fields = ('name', )
    lookup_field = 'slug'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAdminOrReadOnly)


class GenresViewSet(CategoriesViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend, DjangoFilterBackend, )
    filterset_class = TitleFilter
    filterset_fields = ('name', )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAdminOrReadOnly, )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializer
        return CreateTitleSerializer


def get_title(title_id) -> Title:
    return get_object_or_404(Title, pk=title_id)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrStaffOrReadOnly, )

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        queryset = title.reviews.all()
        return queryset

    def perform_create(self, serializer) -> None:
        title = get_title(self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrStaffOrReadOnly, )

    def get_queryset(self) -> QuerySet:
        review = get_object_or_404(
            Review, pk=self.kwargs.get('review_id', 'title_id'))
        return review.comments.all()

    def perform_create(self, serializer) -> None:
        title = get_title(self.kwargs['title_id'])
        review = get_object_or_404(
            Review, pk=self.kwargs.get('review_id', 'title_id'))
        serializer.save(
            author=self.request.user, title=title, review=review)
        # проверку добавили, но мы не можем убрать title,
        # это необходимое поле в модели


class UserViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'username'
    permission_classes = (IsAuthenticated, IsAdminOrDeny, )
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('username', )


@decorators.api_view(('GET', 'PATCH', ), )
@decorators.permission_classes([IsAuthenticated, IsOwnerOrReadOnly])
def api_get_profile(request):
    if request.method == 'GET':
        serializer = MyOwnProfileSerializer(request.user)
        return Response(serializer.data, status=200)
    elif request.method == 'PATCH':
        serializer = MyOwnProfileSerializer(instance=request.user,
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
