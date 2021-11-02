from operator import ge, le
from accounts.models import History
from movies.models import Movie
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
from scipy import sparse


def standardize(row):
    new_row = (row - row.mean())/(row.max()-row.min())
    return new_row


def colaborative_filtering(his, user):
    all_his = History.objects.all().values_list()
    arr = np.array(all_his)
    arr = np.concatenate((arr[:, 2:3], arr[:, 1:2], arr[:, 3:4]), axis=1)
    arr = np.array(arr, dtype=int)
    arr_unique = np.unique(arr[:, 1], return_index=True)
    arr = np.split(arr, arr_unique[1])
    arr = arr[1:]
    user = arr_unique[0]
    arr = [x.transpose() for x in arr]
    arr = [np.concatenate((x[0:1, :], x[2:, :]), axis=0) for x in arr]
    sample = []
    us = 0
    for x in arr:
        sample.append(pd.DataFrame(x[1:], columns=x[0], index=[user[us]]))
        us += 1
    arr = sample
    print(arr)
    arr = arr[0].append(arr[1])
    ratings = arr.fillna(0)
    df_std = ratings.apply(standardize).T
    sparse_df = sparse.csr_matrix(df_std.fillna(0).values)
    corrMatrix = pd.DataFrame(cosine_similarity(
        sparse_df), index=ratings.columns, columns=ratings.columns)
    corrMatrix = ratings.corr(method='pearson')
    print(corrMatrix)


def recommend_movies(history, user):
    colaborative_filtering(history, user)
    his = np.array(history.values_list('movies'))
    his = his.reshape(1, -1)[0]
    qs = Movie.objects.all()
    vlqs = qs.values_list()
    vlqs = np.array(vlqs)
    vlqs = np.concatenate(
        (vlqs[:, 1:2], vlqs[:, 5:6]), axis=1)
    vlqs = np.apply_along_axis(lambda row: " ".join(row),
                               axis=1,
                               arr=vlqs)
    cv = CountVectorizer()
    cv_matrix = cv.fit_transform(list(vlqs))
    score = cosine_similarity(cv_matrix)
    total_score = []
    for i in his:
        total_score += list(enumerate(score[int(i) - 1]))
    score = sorted(total_score,
                   reverse=True, key=lambda x: x[1])[:len(his) + 6]
    score = list(filter(lambda x: x[0]+1 not in his, score))
    print(score)
    return Movie.objects.filter(pk__in=[i[0] + 1 for i in score])
