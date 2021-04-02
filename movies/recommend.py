from movies.models import Movie
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import math


def recommend_movies(list_movies):
    qs = Movie.objects.all()
    similar = []
    for movie in list_movies:
        arr = []
        for q in qs:
            string = q.name + ' ' + q.director.name + ' ' + q.cast
            for g in q.genre.all():
                string += ' ' + g.genre
            arr.append(string)
        cv = CountVectorizer()
        countMat = cv.fit_transform(arr)
        similarity_cos = cosine_similarity(countMat)
        id = movie.id
        similar_movies = list(enumerate(similarity_cos[id-1]))
        similar += similar_movies
    sorted_similar_mov = sorted(similar,key=lambda x:x[1],reverse=True)
    print(sorted_similar_mov)
    count = 0
    l = []
    for id in sorted_similar_mov:
        if math.floor(id[1]) != 1:
            print(id[0])
            l.append(Movie.objects.filter(pk=(id[0]+1)).first())
            count+=1
            if count>2:
                break
    return l