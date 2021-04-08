from operator import ge, le
from accounts.models import History, Profile
from movies.models import Movie
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import math


def recommend_CB(list_movies):
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
    return similar
    
def get_similar_user(list_watch,user):
    all_user = Profile.objects.all().order_by('id')
    watch_history = History.objects.filter(user=user)
    list1 = []
    for user in all_user:
        l = []
        for movie in Movie.objects.all().order_by('id'):
            q = watch_history.filter(pk=movie.id)
            if q.exists():
                l.append(q.first().user_rating)
            else:
                l.append(0)
        list1.append(l)
        list2 = []
        for row in list1:
            l = []
            for val in row:
                k = (val - (sum(row)/len(row)))/(max(row)-min(row))
                l.append(k)
            list2.append(l)
        similar_history = cosine_similarity(list2)
        positive_list = sorted(enumerate(similar_history[user.id-1]),key=lambda x:x[1],reverse=True)
        positive_list = filter(lambda x: x[1]>0 and x[1]!=similar_history[user.id-1][user.id-1],positive_list)
        return positive_list

def transpose(l1):
    l2 = []
    for i in range(len(l1[0])):
        row =[]
        for item in l1:
            row.append(item[i])
        l2.append(row)
    return l2

def get_similar_user_item(list_watch,user):
    all_user = Profile.objects.all().order_by('id')
    watch_history = History.objects.filter(user=user)
    list1 = []
    for user in all_user:
        l = []
        for movie in Movie.objects.all().order_by('id'):
            q = watch_history.filter(pk=movie.id)
            if q.exists():
                l.append(q.first().user_rating)
            else:
                l.append(0)
        list1.append(l)
        list2 = []
        for row in list1:
            l = []
            for val in row:
                k = (val - (sum(row)/len(row)))/(max(row)-min(row))
                l.append(k)
            list2.append(l)
    list2 = transpose(list2)
    similar_history = cosine_similarity(list2)
    # print(similar_history)
    return similar_history
    # print(list2)

def get_similar_movies(movie,rating,similar_user):
    similar_score = list(enumerate(similar_user[movie]*(rating - 2.5)))
    # similar_score = sorted(similar_score,key=lambda x:x[1],reverse=True)
    return similar_score

def user_recomend(list_watch,user):
    similar_user = get_similar_user_item(list_watch,user)
    user_history = History.objects.filter(user=user)
    list3 = []
    for movies in user_history:
        list3.append(get_similar_movies(movies.movies.id-1,movies.user_rating,similar_user))
    l = []
    print(list3)
    length = Movie.objects.all().count()
    no_of_user = len(list_watch)
    i = 0
    while i<length:
        j = 0
        sum = 0
        while j<no_of_user:
            sum += list3[j][i][1]
            j+=1
        l.append((i,sum))
        i += 1
    l = sorted(l,key=lambda x:x[1],reverse=True)
    print(l)
    return l


def generalize_list(l):
    l = sorted(l,key=lambda x:x[0])
    d = {}
    d_c = {}
    for k,v in l:
        d[k] = d.get(k,0) + v
        d_c[k] = d_c.get(k,0) + 1
    l = []
    for k in d:
        l.append((k,d[k]/d_c[k]))
    return sorted(l,key=lambda x:x[1],reverse=True)

def combine(l1,l2):
    l1 = sorted(l1,key=lambda x:x[0],reverse=True)
    l2 = sorted(l2,key=lambda x:x[0],reverse=True)
    k = len(l1)
    l3 = []
    for l in range(k):
        l3.append((l,l1[l][1]+l2[l][1]))
    return sorted(l3,key=lambda x:x[1],reverse=True)

def recommend_movies(list_watch,user):
    l = user_recomend(list_watch,user)
    list_ = sorted(recommend_CB(list_watch),key=lambda x:x[1],reverse=True)
    list_ = list(filter(lambda x:math.floor(x[1]) != 1,list_))
    list_ = generalize_list(list_)
    list_ = combine(l,list_)
    print(list_)
    k = []
    count = 0
    for id in list_:
        if math.floor(id[1]) != 1:
            k.append(Movie.objects.filter(pk=(id[0]+1)).first())
            count+=1
            if count>2:
                break
    return k