from rest_framework import serializers
from .models import History

class HistorySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_user')
    movies = serializers.SerializerMethodField('get_movie_name')
    class Meta:
        model = History
        fields = ['id','movies','user','user_rating','comments']
    def get_user(self,obj):
        return obj.user.user.username
    def get_movie_name(self,obj):
        return obj.movies.name

class HistoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['movies','user_rating','comments']