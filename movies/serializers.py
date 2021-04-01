from rest_framework import serializers
from .models import Director, Genre, Movie

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id','genre']

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id','name']

class MovieSerializer(serializers.ModelSerializer):
    genre = serializers.SerializerMethodField('get_genre')
    director = DirectorSerializer(read_only=True)
    likes = serializers.SerializerMethodField('get_likes')
    class Meta:
        model = Movie
        fields = ['name','file','poster','rating','director','cast','genre','likes']
    def get_likes(self,obj):
        return obj.likes.count()
    def get_genre(self,obj):
        return GenreSerializer(obj.genre,many=True).data