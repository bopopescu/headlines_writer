from flask import Flask
from flask import jsonify
from flask import send_from_directory, request, Response
from flask import render_template
import title_generator as TG
import json, random, mongo_config
#from forms import LoginForm

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
    return json.dumps({'generated': generated_title,
                       'real': real_title}, ensure_ascii=False).encode('utf8'),  200




@app.route("/input_word", methods = ['GET', 'POST'])
def input_word():

	try:
		lang = request.args.get('inputword', 0, type=str)
		if lang.lower() == 'python':
			return json.dumps([{'simword':'hi', 'value': 0.8}])
		else:
			return json.dumps([{'simword':'hello', 'value': 0.9}])

	except Exception as e:
		return str(e)


if __name__ == "__main__":
    app.run()

