from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.db.models import Avg
from rest_framework.fields import CurrentUserDefault
from rest_framework.validators import UniqueTogetherValidator
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
    rating = serializers.SerializerMethodField(default=None)

    def get_rating(self, obj):
        return obj.reviews.aggregate(Avg('score'))['score__avg']

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category', 'rating', )
        model = Title


class CreateTitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(slug_field='slug', queryset=Genre.objects.all(), many=True, required=False)
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())

    class Meta:
        fields = ('id', 'category', 'genre', 'name', 'year', 'description')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=CurrentUserDefault(),
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
'''        validators = (
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('title', 'author')
            ),
        )'''


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
