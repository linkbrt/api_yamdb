from django.contrib.auth import get_user_model
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from .models import Category, Comment, Confirm, Genre, Profile, Review, Title
from .validators import IsExistsValidator

User = get_user_model()


class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
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
        if self.context['request'].method != 'PATCH':
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


STAFF_GROUPS = ('moderator', 'admin')


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'username',
                  'email', 'bio', 'role')


class MyOwnProfileSerializer(ProfileSerializer):

    def validate_role(self, value):
        user = self.context['request'].user
        if user.role == 'admin':
            return value
        if user.role == 'moderator':
            return 'moderator'
        return 'user'


class CreateConfirmCodeSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.HiddenField(default='')

    class Meta:
        model = Confirm
        fields = ('email', 'confirmation_code', )


class RetrieveTokenSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = Confirm
        fields = '__all__'
        validators = [
            IsExistsValidator(
                fields=('email', 'confirmation_code', )
            )
        ]