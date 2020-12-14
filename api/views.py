from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, viewsets, generics, status
from rest_framework.response import Response
from users.permissions import (IsAdminOrDeny, IsAdminOrReadOnly, IsOwnerOrStaffOrReadOnly,
                               IsStaffOrReadOnly)
from rest_framework.response import Response
from .models import Category, Genre, Review, Title
from .serializers import (CategorieSerializer, CommentSerializer, 
                          CreateTitleSerializer, GenreSerializer, 
                          ReviewSerializer, TitleSerializer)
from .filters import TitleFilter
from rest_framework.filters import SearchFilter


class CategoriesViewSet(viewsets.ViewSet, generics.CreateAPIView, 
                        mixins.ListModelMixin, mixins.DestroyModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorieSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name', ]
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAdminOrReadOnly]


class GenresViewSet(viewsets.ViewSet, generics.CreateAPIView, 
                    mixins.ListModelMixin, mixins.DestroyModelMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer    
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name', ]
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, 
                          IsAdminOrReadOnly]


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = TitleFilter
    filterset_fields = ['name']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, 
                          IsAdminOrReadOnly]

    def get_queryset(self):
        return super().get_queryset().order_by('-id')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializer
        return CreateTitleSerializer


    """ def create(self, request, *args, **kwargs):
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
                        headers=headers) """


class ReviewViewSet(viewsets.ModelViewSet):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrStaffOrReadOnly, ]
    # lookup_field = 'id'

    def get_queryset(self):
        queryset = get_object_or_404(Title, pk=self.kwargs['title_id']).reviews.all()
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrStaffOrReadOnly, )
    # lookup_field = 'id'

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(
            author=self.request.user, title=title, review=review)