from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Category, Comment, Genre, Review, Title


User = get_user_model()


class CategorieSerializer(serializers.ModelSerializer):

    class Meta:
        # fields = '__all__'
        model = Category
        fields = ['name', 'slug']        


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        # fields = '__all__'
        model = Genre
        fields = ['name', 'slug']


class TitleSerializer(serializers.ModelSerializer):

    # category = CategorieSerializer()
    # genre = GenreSerializer(many=True, read_only=True)

    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True)
    category = serializers.SlugRelatedField(
        slug_field='slug',queryset=Category.objects.all())

    class Meta:
        # fields = '__all__'
        fields = ['name', 'year', 'description', 'genre', 'category']
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )

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
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        # fields = '__all__'
        fields = ['id', 'text', 'author', 'pub_date']
