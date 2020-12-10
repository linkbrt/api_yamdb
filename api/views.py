from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, viewsets

from .models import Category, Genre, Review, Title
from .serializers import (CategorieSerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer)
from users.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly, IsStaffOrReadOnly


class DefaultViewSet(
            viewsets.ModelViewSet,
            mixins.CreateModelMixin,
            mixins.DestroyModelMixin,
            mixins.ListModelMixin):
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]


class CategoriesViewSet(DefaultViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorieSerializer


class GenresViewSet(DefaultViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitlesViewSet(DefaultViewSet,
            mixins.RetrieveModelMixin,
            mixins.UpdateModelMixin):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
                'category',
                'genre',
                'name',
                'year'
                ]


def get_title(self):
    title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
    return title


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, IsStaffOrReadOnly]

    def queryset(self):
        title = get_title(self)
        queryset = title.reviews.all()
        return queryset

    def perform_create(self, serializer):
        title = get_title(self)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, IsStaffOrReadOnly]

    def queryset(self):
        title = get_title(self)
        queryset = title.reviews.all()
        return queryset

    def perform_create(self, serializer):
        title = get_title(self)
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(
            author=self.request.user, title=title, review=review)
