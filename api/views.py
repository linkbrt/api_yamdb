from rest_framework import viewsets, mixins
from rest_framework import permissions
from .models import Categories, Genres, Titles
from .serializers import CategorieSerializer, GenreSerializer, TitleSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


class BaseListCreateDestroyViewSet(
            viewsets.ModelViewSet, 
            mixins.CreateModelMixin,
            mixins.DestroyModelMixin,
            mixins.ListModelMixin):
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']


    #def get_permissions(self):
        #if self.action == 'list':
            #permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        #else:
            #permission_classes = [permissions.IsAdminUser]


class CategoriesViewSet(BaseListCreateDestroyViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorieSerializer


class GenresViewSet(BaseListCreateDestroyViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer


class TitlesViewSet(BaseListCreateDestroyViewSet,
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