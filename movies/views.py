from django.db import models
from accounts.models import Profile,History
from django.http.response import Http404
from movies.serializers import DirectorSerializer, GenreSerializer, MovieCreateSerializer, MovieSerializer
from movies.models import Director, Movie,Genre
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from accounts.serializers import HistorySerializer
from .recommend import recommend_movies

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
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

@api_view(['GET'])
def movie_search(request):
    try:
        str = request.GET['str']
    except:
        return Response({'message':'not valid'},status=400)
    qs = Movie.objects.filter(name__contains=str)
    if qs.exists():
        return Response(MovieSerializer(qs,many=True).data,status=200)
    return Response({'message':'Movie not found'},status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_movie(request):
    dir = request.data.get('director')
    genre = str(request.data.get('genre')).split(" ")
    # print(genre)
    serial = MovieCreateSerializer(data=request.data or None)
    if serial.is_valid():
        if not Director.objects.filter(name=dir).exists():
            Director(name=dir).save()
        dir = Director.objects.filter(name=dir).first()
        u = serial.save(director=dir,upload_by=Profile.objects.filter(user=request.user).first())        
        m = Movie.objects.filter(name=serial.data['name']).first()
        for g in genre:
            qs = Genre.objects.filter(genre=g)
            if qs.exists():
                qs = qs.first()
            else:
                qs = Genre(genre=g)
                qs.save()
            m.genre.add(qs)
        return Response({'message':'Success'},status=201)
    return Response({},status=400)

    '''
    {
        "name": "Damn",
        "file": "Damn",
        "poster": "Damn",
        "rating": 9.9,
        "director": "Shreesh",
        "cast": "Shreesh Srivastava",
        "genre":"Damn KK"
    }
'''

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def genre_list(request):
    qs = Genre.objects.all()
    serial = GenreSerializer(qs,many=True)
    return Response(serial.data,status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def director_list(request):
    qs = Director.objects.all()
    serial = DirectorSerializer(qs,many=True)
    return Response(serial.data,status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend(request):
    user = request.user
    qs = History.objects.filter(user=Profile.objects.filter(user=user).first())
    watched_movies = list()
    for q in qs:
        watched_movies.append(q.movies)
    qs = recommend_movies(watched_movies)
    # serial = MovieSerializer(qs,many=True)
    data = []
    for l in qs:
        s = MovieSerializer(l)
        data.append(s.data)
    return Response(data,status=200)