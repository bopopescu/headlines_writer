import nltk, re, mongo_config
from nltk.tokenize import RegexpTokenizer

titles = mongo_config.titles

#tokenize
tokenizer = RegexpTokenizer(r"\w+[^\w\s]?\w+")
tokenized_titles = []
for title in titles:
    tokenized = tokenizer.tokenize(title)
    tokenized_titles.append(tokenized)

#write tokens to file
thefile = open('tokenized_titles.txt', 'w')
thefile.write(str(tokenized_titles))
thefile.close()

#tag
tagged_titles = []
for title in tokenized_titles:
    tagged = nltk.pos_tag(title)
    tagged_titles.append(tagged)

#write tags to file
thefile = open('tagged_titles.txt', 'w')
thefile.write(str(tagged_titles))
thefile.close()

