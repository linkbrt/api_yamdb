from django.core.validators import EmailValidator
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from .models import Category, Comment, Genre, Profile, Review, Title


class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        lookup_field = 'slug'
        fields = ['name', 'slug']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name', 'slug']


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True, )
    category = CategorieSerializer()
    rating = serializers.SerializerMethodField(
        default=None,
    )

    def get_rating(self, obj):
        return obj.reviews.aggregate(Avg('score'))['score__avg']

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description',
                  'genre', 'category')
        model = Title


class CreateTitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True, required=False,
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    class Meta:
        fields = '__all__'
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
        if self.context['request'].method != 'POST':
            return data

        title_id = self.context['view'].kwargs.get('title_id')
        user = self.context['request'].user
        if Review.objects.filter(title=title_id, author=user).exists():
            raise serializers.ValidationError('Error double', code=400)

        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'title',
                  'author', 'score', 'pub_date', )


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


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'username',
                  'email', 'bio', 'role')


class CreateProfileSerializer(serializers.ModelSerializer):
    """
    Default email field raise exception
    if user with this email already exists
    """
    email = serializers.CharField(validators=[EmailValidator])

    class Meta:
        model = Profile
        fields = ('email', )


class RetrieveTokenSerializer(serializers.ModelSerializer):
    """Just like in CreateProfileSerializer"""
    email = serializers.CharField(validators=[EmailValidator])
    confirmation_code = serializers.CharField()

    class Meta:
        model = Profile
        fields = ('email', 'confirmation_code', )
