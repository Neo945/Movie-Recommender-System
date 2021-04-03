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
    
def is_similar(qs,user_history):
    similarity_count = 0
    list_ = []
    for q in qs.order_by('id'):
        if user_history.filter(movies=q.movies).exists():
            similarity_count+=1

    for uh in user_history.order_by('id'):
        if not qs.filter(movies=uh.movies).exists():
            list_.append(uh.movies.id)
    if similarity_count==0:
        return (False,None)
    else:
        return (True,list_)

def user_recommend(user):
    qs = History.objects.filter(user=user).order_by('id')
    all_qs = History.objects.all()
    profile_qs = Profile.objects.all()
    for profile in profile_qs:
        user_history = all_qs.filter(user=profile).order_by('id')
        (is_sim,next) = is_similar(qs,user_history)
        if is_sim:
            print(next)
            return next
    return None

def recommend_movies(list_watch,user):
    cb_list = recommend_CB(list_watch)
    user_list = user_recommend(user=user) or []
    for data in cb_list:
        if data[0]+1 in user_list:
            # Doubt
            pass
    k = []
    count = 0
    list_ = sorted(cb_list,key=lambda x:x[1],reverse=True)
    for id in list_:
        if math.floor(id[1]) != 1:
            k.append(Movie.objects.filter(pk=(id[0]+1)).first())
            count+=1
            if count>2:
                break
    return k