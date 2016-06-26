# -*- coding: utf-8 -*-
from flask import Flask
from flask import jsonify
from flask import send_from_directory, request, Response
from flask import render_template
import title_generator as TG
import json, random, mongo_config
import gensim
from gensim.corpora import WikiCorpus
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

app = Flask(__name__)
vector_file = "data/all_vector"
model = gensim.models.Word2Vec.load_word2vec_format(vector_file, binary=False)

def get_sim_words(word, model):

    try:
        ret = model.most_similar(word)

    except Exception, e:
        print e


    res = []
    for item in ret:
        res.append(item[0].encode('utf-8'))

    return res


@app.after_request
def add_header(response):
    response.cache_control.max_age = 0
    return response

@app.route("/")
def index():
    return render_template('index.html'), 200

@app.route("/generate")
def generate_title():
    real_title = random.choice(mongo_config.titles)
    generator = TG.TitleGenerator()
    generated_title = generator.generate_title()
    return json.dumps({'generated': generated_title,
                       'real': real_title}, ensure_ascii=False).encode('utf8'),  200




@app.route("/input_word", methods = ['GET', 'POST'])
def input_word():
    try:
        inputword = request.args.get('inputword')
        print "lookfor word: %s" % inputword

        sim_words = get_sim_words(inputword, model)
        print "found %d sim words" % len(sim_words)

        return json.dumps([{'simword': "\n".join(sim_words), 'value': 0.8}])


    except Exception as e:
        print "exception : %s" % str(e)
        return str(e)


if __name__ == "__main__":
    app.run()

