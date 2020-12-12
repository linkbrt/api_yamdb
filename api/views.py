from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, viewsets, generics
from rest_framework.response import Response
from users.permissions import (IsAdminOrDeny, IsAdminOrReadOnly, IsOwnerOrReadOnly,
                               IsStaffOrReadOnly)

from .models import Category, Genre, Review, Title
from .serializers import (CategorieSerializer, CommentSerializer, CreateTitleSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer)


class DefaultViewSet(
            viewsets.ModelViewSet,
            mixins.CreateModelMixin,
            mixins.DestroyModelMixin,
            mixins.ListModelMixin):
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['=name', ]
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]


class CategoriesViewSet(viewsets.ViewSet, generics.CreateAPIView, mixins.ListModelMixin, mixins.DestroyModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorieSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name', ]
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]


class GenresViewSet(viewsets.ViewSet, generics.CreateAPIView, mixins.ListModelMixin, mixins.DestroyModelMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name', ]
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]


class TitlesViewSet(viewsets.ViewSet, generics.ListCreateAPIView, mixins.DestroyModelMixin):
    queryset = Title.objects.all()
    serializer_class = CreateTitleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
                'category',
                'genre',
                'name',
                'year'
                ]

    def create(self, request, *args, **kwargs):
        in_data = {**request.data}
        for key, value in in_data.items():
            in_data[key] = value[0]
        in_data['genre'] = request.data['genre'].split(', ')
        serializer = CreateTitleSerializer(data=in_data)
        serializer.is_valid(True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly, IsStaffOrReadOnly]
    # lookup_field = 'id'

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        queryset = title.reviews.all()
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly, IsStaffOrReadOnly]
    # lookup_field = 'id'

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        queryset = review.comments.all()
        # queryset = Comment.objects.filter(review=review)
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(
            author=self.request.user, title=title, review=review)
