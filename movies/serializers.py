from rest_framework import serializers
from .models import Director, Genre, Movie
from accounts.models import Profile

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
    class Meta:
        model = Movie
        fields = ['id','name','poster','rating','director','cast','genre','description']
    
    def get_likes(self,obj):
        return obj.likes.count()
    def get_genre(self,obj):
        return GenreSerializer(obj.genre,many=True).data
    def get_user(self,obj):
        return Profile.objects.filter(pk=obj.upload_by.id).first().user.username

class MovieCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['name','poster','rating','cast','description']