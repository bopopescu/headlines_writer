import nltk, re, pprint
import random
import pymongo
import itertools
from textstat.textstat import textstat
from nltk.tokenize import RegexpTokenizer

from nltk.parse.generate import generate
from nltk import CFG

MONGODB_SERVER = "localhost"
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

rand = random.randint(0, len(titles) - 100) 
titles = titles[rand:rand+100]

min_title_length = 5
max_title_length = 5
for title in titles:
    length = len(title.split())

    if length > max_title_length:
        max_title_length = length

    if length < min_title_length:
        min_title_length = length


#tokenize
tokenizer = RegexpTokenizer(r"\w+[^\w\s]?\w+")
starting_words = []
tokenized_titles = []
for title in titles:
    tokenized = tokenizer.tokenize(title)
    tokenized_titles.append(tokenized)

#tag
#tagged_titles = []
#for title in tokenized_titles:
#    tagged = nltk.pos_tag(title)
#    tagged_titles.append(tagged)
#
#thefile = open('tagged_titles.txt', 'w')
#thefile.write(str(tagged_titles))
#thefile.close()

def generate_model(cfd, word, num=random.randint(min_title_length, max_title_length)):
    generated_title = word + ' '
    for i in range(num):
        if (cfd[word]):
            word = random.choice(cfd[word].most_common(3))[0]
            generated_title += word + ' '
        else:
            break
    return generated_title

all_bigrams = []
first_words = []
for title in tokenized_titles:
    first_words.append(title[0])
    all_bigrams.append(nltk.bigrams(title))

flat_all_bigrams = list(itertools.chain(*all_bigrams))
cfd = nltk.ConditionalFreqDist(flat_all_bigrams) 

