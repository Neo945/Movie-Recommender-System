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
    similar_score = enumerate(similar_user[movie]*(rating - 2.5))
    similar_score = sorted(similar_score,key=lambda x:x[1],reverse=True)
    return similar_score

def user_recomend(list_watch,user):
    similar_user = get_similar_user_item(list_watch,user)
    user_history = History.objects.filter(user=user)
    list3 = []
    for movies in user_history:
        list3.append(get_similar_movies(movies.movies.id-1,movies.user_rating,similar_user))
    l = []
    # length = len(list3[0])
    # for k in range(length):
    #     sum = 0
    #     for m in range(len(list3)):
    #         sum += list3[m][k][1]
    #     l.append((k,sum))
    # print(l)
    print(list3)
    i = 0
    # for k in list3[0]:
    #     j = 0
    #     sum = 0
    #     while j<len(k):
    #         if i == k[j]:
    #             sum += k[j]
    #         j+=1
    #     l.append((i,sum))
    #     i+=1
    # print(l)
    return l

def recommend_movies(list_watch,user):
    cb_list = recommend_CB(list_watch)
    k = []
    user_recomend(list_watch,user)
    count = 0
    list_ = sorted(cb_list,key=lambda x:x[1],reverse=True)
    for id in list_:
        if math.floor(id[1]) != 1:
            k.append(Movie.objects.filter(pk=(id[0]+1)).first())
            count+=1
            if count>2:
                break
    return k