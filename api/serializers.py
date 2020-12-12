from django.contrib.auth import get_user_model
from rest_framework import serializers
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
        slug_field='slug', queryset=Category.objects.all())

    class Meta:
        fields = ('id', 'category', 'genre', 'name', 'year', )
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

    # def validate(self, data):
    #     # req = data.get('request.method')
    #     # print(req)
    #     # if data.get('request.method') != 'PATCH':
    #     title_id = self.context['view'].kwargs.get('title_id')
    #     user = self.context['request'].user
    #     if Review.objects.filter(title=title_id, author=user).exists():
    #         raise serializers.ValidationError('Error double', code=400)
    #     return data

    def validate(self, data):
        """
        Защищаеся от дублей и неправильных оценок
        """
        print(self)
        if self.context['request'].method == 'POST':
            if Review.objects.filter(
                    author=self.context['request'].user,
                    title_id=self.context['view'].kwargs.get('title_id'),
            ).exists():
                raise serializers.ValidationError(
                    'Double posting is not allowed'
                )

        return data

    class Meta:
        model = Review
        fields = '__all__'
        # fields = ['id', 'text', 'title', 'author', 'score', 'pub_date']


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
