from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from serializers import CommentSerializer, ReviewSerializer

from .models import Review, Title


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
