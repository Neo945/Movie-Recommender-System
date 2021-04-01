from django.db import models
from movies.serializers import MovieSerializer
from movies.models import Movie,Genre
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

# Create your views here.
@api_view(['GET'])
def all_movies(request):
    qs = Movie.objects.all()
    serial = MovieSerializer(qs,many=True)
    return Response(serial.data,status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def movie_details(request,movie_id):
    qs = Movie.objects.filter(pk=movie_id).first()
    return Response(MovieSerializer(qs).data,status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def genre_movie(request,genre_id):
    if Genre.objects.filter(pk=genre_id).exists():
        if Movie.objects.filter(genre=Genre.objects.filter(pk=genre_id).first()).exists():
            qs = Movie.objects.filter(genre=Genre.objects.filter(pk=genre_id).first()).first()
            return Response(MovieSerializer(qs).data,status=200)
        return Response({'message':'Movie Not Found'},status=404)
    return Response({'message':'Not a valid Genre'},status=404)