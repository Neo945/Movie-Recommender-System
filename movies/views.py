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
        dir = Director.objects.get_or_create(name=dir)
        u = serial.save(director=dir,upload_by=Profile.objects.filter(user=request.user).first())        
        m = Movie.objects.filter(name=serial.data['name']).first()
        for g in genre:
            qs = Genre.objects.get_or_create(genre=g)
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
    if not qs.exists():
        return Response(MovieSerializer(Movie.objects.all().order_by("?"),many=True).data,status=200)
    print('data3')
    watched_movies = list()
    for q in qs:
        watched_movies.append(q.movies)
    qs = recommend_movies(watched_movies,Profile.objects.filter(user=request.user).first())
    print('data5')
    data = []
    for l in qs:
        if not l in watched_movies:
            s = MovieSerializer(l)
            data.append(s.data)
    print(data)
    return Response(data,status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_popular(request):
    hqs = History.objects.filter(user=Profile.objects.filter(user=request.user).first()).values_list('movies',flat=True)
    top_rated_movies = Movie.objects.all().order_by("-rating")
    data = []
    for m in top_rated_movies:
        if not m.id in hqs:
            data.append(MovieSerializer(m).data)
    return Response(data,status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_genre_popular(request):
    hqs = History.objects.filter(user=Profile.objects.filter(user=request.user).first()).order_by('-user_rating').first().movies
    hqs2 = History.objects.filter(user=Profile.objects.filter(user=request.user).first()).values_list('movies',flat=True)
    qs = Movie.objects.filter(genre=hqs.genre.all().order_by("?").first().id).order_by('rating')
    data = []
    print(hqs2)
    for m in qs:
        if not m.id in hqs2:
            data.append(MovieSerializer(m).data)
    return Response(data,status=200)
