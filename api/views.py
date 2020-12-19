from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (decorators, filters, generics, mixins, permissions,
                            status, viewsets)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from .models import Category, Genre, Profile, Review, Title
from .permissions import (IsAdminOrDeny, IsAdminOrReadOnly, IsOwnerOrReadOnly,
                          IsOwnerOrStaffOrReadOnly)
from .serializers import (CategorieSerializer, CommentSerializer,
                          CreateProfileSerializer, CreateTitleSerializer,
                          GenreSerializer, ProfileSerializer,
                          RetrieveTokenSerializer, ReviewSerializer,
                          TitleSerializer)


class BaseListCreateDestroyViewSet(
        viewsets.ViewSet,
        generics.CreateAPIView,
        mixins.ListModelMixin,
        mixins.DestroyModelMixin):
    pass


class CategoriesViewSet(BaseListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorieSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend,)
    search_fields = ('name', )
    lookup_field = 'slug'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAdminOrReadOnly)


class GenresViewSet(BaseListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend,)
    search_fields = ('name', )
    lookup_field = 'slug'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAdminOrReadOnly)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend, DjangoFilterBackend, )
    filterset_class = TitleFilter
    filterset_fields = ('name', )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAdminOrReadOnly, )

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('-id')

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

    def get_queryset(self) -> QuerySet:
        return get_object_or_404(
                    Title,
                    pk=self.kwargs['title_id']
                ).reviews.all()

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
        return review.comments.all() # noqa

    def perform_create(self, serializer) -> None:
        title = get_title(self.kwargs['title_id'])
        review = get_object_or_404(
            Review, pk=self.kwargs.get('review_id', 'title_id'))
        serializer.save(
            author=self.request.user, title=title, review=review)


class UserViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'username'
    permission_classes = (IsAuthenticated, IsAdminOrDeny, )
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username']

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().order_by('-id')

    @decorators.action(
        methods=('GET', 'PATCH', ), detail=False,
        permission_classes=(IsAuthenticated, IsOwnerOrReadOnly, ))
    def me(self, request, *args, **kwargs) -> Response:
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(
            instance=request.user, data=request.data,
            partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@decorators.permission_classes([AllowAny])
@decorators.api_view(['POST'])
def register_user(request):
    serializer = CreateProfileSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    user = Profile.objects.get_or_create(email=email)
    code = default_token_generator.make_token(user[0])
    send_mail('Confirmation code', code,
              None, [email], )
    return Response(data='Mail with confirmation code created.',
                    status=status.HTTP_200_OK)


@decorators.permission_classes([AllowAny])
@decorators.api_view(['POST'])
def retrieve_token(request):
    serializer = RetrieveTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    username = data['email'].split('@')[0]
    user = Profile.objects.get(email=data['email'])
    if not user:
        user = Profile.objects.create(username=username, email=data['email'])
    if default_token_generator.check_token(user, data['confirmation_code']):
        token = 'token: ' + str(RefreshToken.for_user(user).access_token)
        return Response(data=token,
                        status=status.HTTP_200_OK)
    else:
        return Response(data={'confirmation_code': ['not valid', ]},
                        status=status.HTTP_400_BAD_REQUEST)