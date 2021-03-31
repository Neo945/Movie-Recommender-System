from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sqlite3


conn = sqlite3.connect('movies.db')
cur = conn.execute("""SELECT "title","genres","cast","director" FROM mytable order by "indexI";""")
arr = []
for row in cur:
    stri = ""
    if row[0] != None:
        stri = row[0]
    if row[1] != None:
        stri = stri + " " + row[1]
    if row[2] != None:
        stri = stri + " " + row[2]
    if row[3] != None:
        stri = stri + " " + row[3]
    arr.append(stri)

print(arr)
cv = CountVectorizer()
countMat = cv.fit_transform(arr)
print(countMat.toarray())
similarity_cos = cosine_similarity(countMat)
print(similarity_cos)
like = """ "Star Wars: Episode III - Revenge of the Sith" """
statement = """select "indexI" from mytable where "title" =  """ + like + """;"""
cur = conn.execute(statement)
k = None
for row in cur:
    k = int(row[0])
print(similarity_cos[k])
similar_movies = list(enumerate(similarity_cos[k]))
print(similar_movies)
sorted_similar_mov = sorted(similar_movies,key=lambda x:x[1],reverse=True)
print(sorted_similar_mov)
i = 0
for mov in sorted_similar_mov:
    cur = conn.execute("""select "title" from mytable where "indexI" =  """ + str(mov[0]) + """;""")
    for row in cur:
        print(row[0])
    i = i+1
    if i>10:
        break