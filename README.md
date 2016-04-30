#Click Bait Title Generator:
- Make sure you have the required dependencies installed
`pip install -r requirements.txt`
- Install the NLTK packages punkt, stopwords and tagsets from python shell:

				>>> import nltk
 				>>> nltk.download()
- [Install](https://docs.mongodb.org/v3.0/administration/install-on-linux/) mongodb and import mongodb database dump:
`mongorestore --collection posts --db buzzfeed dump/buzzfeed/posts.bson`
- Run flask webserver with `python click_bait.py`
- Direct your browser to the [webserver](http://127.0.0.1:5000/)
- Click Generate

###Info:
- Regenerating tags and tokens can be done by running `python tag_tokenize.py` although this is unecessary.
- The Buzzfeed scraper used can be found [here](https://github.com/fowler446/buzz_scraper)

	



