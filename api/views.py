from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, generics, mixins, permissions, status,
                            viewsets)
from rest_framework.response import Response
from users.permissions import (IsAdminOrReadOnly,
                               IsOwnerOrStaffOrReadOnly, )

from .models import Category, Genre, Review, Title
from .serializers import (CategorieSerializer, CommentSerializer,
                          CreateTitleSerializer, GenreSerializer,
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
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAdminOrReadOnly)


class GenresViewSet(CategoriesViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('category', 'genre',
                        'name', 'year', )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAdminOrReadOnly, )

    def get_queryset(self) -> QuerySet:
        return super().get_queryset()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializer
        return CreateTitleSerializer

    def create(self, request, *args, **kwargs) -> Response:
        in_data = {**request.data}
        for key, value in in_data.items():
            in_data[key] = value[0]
        genre = request.data.get('genre')
        if genre:
            in_data['genre'] = genre.split(', ')
        serializer = CreateTitleSerializer(data=in_data)
        serializer.is_valid(True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)


def get_title(title_id) -> Title:
    return get_object_or_404(Title, pk=title_id)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrStaffOrReadOnly, )

    def get_queryset(self) -> QuerySet:
        return get_title(self.kwargs['title_id']).reviews.all()

    def perform_create(self, serializer) -> None:
        title = get_title(self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrStaffOrReadOnly, )

    def get_queryset(self) -> QuerySet:
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer) -> None:
        title = get_title(self.kwargs['title_id'])
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(
            author=self.request.user, title=title, review=review)
