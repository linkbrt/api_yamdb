from rest_framework import serializers
from .models import Categories, Genres, Titles
from rest_framework.validators import UniqueValidator


class CategorieSerializer(serializers.ModelSerializer):


    class Meta:
        fields = '__all__'
        model = Categories
        #validators = [UniqueValidator(queryset=Categories.objects.all())]


class GenreSerializer(serializers.ModelSerializer):


    class Meta:
        fields = '__all__'
        model = Genres
        #validators = [UniqueValidator(queryset=Genres.objects.all())]


class TitleSerializer(serializers.ModelSerializer):


    class Meta:
        fields = '__all__'
        model = Titles
        #validators = [UniqueValidator(queryset=Titles.objects.all())]