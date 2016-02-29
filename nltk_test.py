import nltk
import random
from nltk.parse.generate import generate
from nltk import CFG

titles = ["14 ways to derp a best friend", "5 ways to shave a cat"] 

#tokenize
tokenized_titles = []
for title in titles:
    tokenized = nltk.word_tokenize(title)
    tokenized_titles.append(tokenized)

#tag
tagged_titles = []
for title in tokenized_titles:
    tagged = nltk.pos_tag(title)
    tagged_titles.append(tagged)

#flatten lists of tagged words
all_tags = [item for sublist in tagged_titles for item in sublist]

#Build tag word map
tag_word_map = {}
for word, tag in all_tags:
    if tag in tag_word_map:
        tag_word_map[tag].append(word)   
    else:
        tag_word_map[tag] = [word]

sentence_structures = []
for word_tag_pair in tagged_titles:
    temp = []
    for pair in word_tag_pair:
        temp.append(pair[1])
    sentence_structures.append(temp)

start_tag_list = random.choice(sentence_structures)
start = str.join(" ", start_tag_list)

#Build CFG
cfg = "S -> " + start + "\n"
for tag in start_tag_list:
    terminal = random.choice(tag_word_map[tag])
    cfg += tag + " -> " + "'" + terminal + "'" + "\n"

grammar = nltk.CFG.fromstring(cfg)
for sentence in generate(grammar):
    print(' '.join(sentence))

