from movies.serializers import MovieSerializer
from movies.models import Movie
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['GET'])
def all_movies(request):
    qs = Movie.objects.all()
    serial = MovieSerializer(qs,many=True)
    return Response(serial.data,status=200)