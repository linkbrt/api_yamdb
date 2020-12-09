from rest_framework import serializers
from .models import Categories, Genres, Titles


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