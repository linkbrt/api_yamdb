from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Categories, Comment, Genres, Review, Titles


User = get_user_model()


class CategorieSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Categories


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genres


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Titles


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username')

    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name')

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        user = self.context['request'].user
        if Review.objects.filter(title=title_id, author=user).exists():
            raise serializers.ValidationError('Error double', code=400)
        return data

    class Meta:
        model = Review
        # fields = '__all__'
        fields = ['id', 'text', 'author', 'score', 'pub_date']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        # fields = '__all__'
        fields = ['id', 'text', 'author', 'pub_date']
