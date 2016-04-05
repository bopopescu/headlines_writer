from flask import Flask
from flask import render_template
import title_generator as TG
import json, random, mongo_config

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
    real_title = random.choice(mongo_config.titles)
    generator = TG.TitleGenerator()
    generated_title = generator.generate_title()
    return json.dumps({'generated': generated_title, 'real': real_title}, ensure_ascii=False).encode('utf8'),  200

if __name__ == "__main__":
    app.run()
