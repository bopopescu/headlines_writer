from flask import Flask
from flask import render_template
import pymongo
import random
import json
import nltk_test

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "buzzfeed"
MONGODB_COLLECTION = "posts"

connection = pymongo.MongoClient(MONGODB_SERVER, MONGODB_PORT)

db = connection[MONGODB_DB]
collection = db[MONGODB_COLLECTION]

titles = []
posts = list(collection.find({}))

app = Flask(__name__)

@app.after_request
def add_header(response):
    response.cache_control.max_age = 0
    return response

@app.route("/")
def index():
    return render_template('index.html'), 200

@app.route("/generate")
def generate_title():
    real_post = random.choice(posts)["post_title"]
    generated_post = nltk_test.generate_title()
    return json.dumps({'generated': generated_post, 'real': real_post}, ensure_ascii=False).encode('utf8'),  200

if __name__ == "__main__":
    app.run()
