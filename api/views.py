from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, viewsets

from .models import Categories, Genres, Review, Title, Titles
from .serializers import (CategorieSerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer)


class DefaultViewSet(
            viewsets.ModelViewSet, 
            mixins.CreateModelMixin,
            mixins.DestroyModelMixin,
            mixins.ListModelMixin):
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']


    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [permissions.IsAdminUser]


class CategoriesViewSet(DefaultViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorieSerializer


class GenresViewSet(DefaultViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer


class TitlesViewSet(DefaultViewSet,
            mixins.RetrieveModelMixin,
            mixins.UpdateModelMixin):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Titles.objects.all()
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
    permission_classes = []

    def queryset(self):
        title = get_title()
        queryset = title.reviews.all()
        return queryset

    def perform_create(self, serializer):
        title = get_title()
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = []

    def queryset(self):
        title = get_title()
        queryset = title.reviews.all()
        return queryset

    def perform_create(self, serializer):
        title = get_title()
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(
            author=self.request.user, title=title, review=review)
