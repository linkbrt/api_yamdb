from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.db.models import Avg
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

    genre = GenreSerializer(many=True, )
    category = CategorieSerializer()

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category', )
        model = Title


class CreateTitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(slug_field='slug', queryset=Genre.objects.all(), many=True, required=False)
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())
    rating = serializers.SerializerMethodField(default=None)

    class Meta:
        fields = ('id', 'category', 'genre', 'name', 'year', 'rating')
        model = Title

    def get_rating(self, obj):
        return Review.objects.annotate(
                rating=Avg('score')
                ).order_by('-id')


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

        if self.context['request'].method != 'PATCH':
            title_id = self.context['view'].kwargs.get('title_id')
            user = self.context['request'].user
            if Review.objects.filter(title=title_id, author=user).exists():
                raise serializers.ValidationError('Error double', code=400)
            return data

    class Meta:
        model = Review
        # fields = '__all__'
        fields = ['id', 'text', 'title', 'author', 'score', 'pub_date']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    review = serializers.SlugRelatedField(
        slug_field='id',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = '__all__'
        # fields = ['id', 'text', 'title', 'author', 'pub_date']
