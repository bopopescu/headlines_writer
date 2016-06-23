import pymongo

MONGODB_SERVER = "127.0.0.1"
MONGODB_PORT = 27017
MONGODB_DB = "buzzfeed"
MONGODB_COLLECTION = "posts"

#setup pymongo
connection = pymongo.MongoClient(MONGODB_SERVER, MONGODB_PORT)

db = connection[MONGODB_DB]
collection = db[MONGODB_COLLECTION]

titles = []
posts = collection.find({})

for post in posts:
    titles.append(post['post_title'].lower().lstrip())
