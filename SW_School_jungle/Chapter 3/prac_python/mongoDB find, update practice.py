from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbjungle 

# 코딩 시작
target_movie = db.movies.find_one({'title':'매트릭스'})
# print(target_movie['star'])

same_star_movies = list(db.movies.find({'star':target_movie['star']}))

# for movie in same_star_movies:
#     print(movie['title'])

db.movies.update_one({'title':'매트릭스'}, {'$set' : {'star': 0}})