import nltk
from textstat.textstat import textstat
import random
from nltk.parse.generate import generate
from nltk import CFG

import tag_generator

thefile = open('tagged_titles.txt', 'r')
tagged_titles = eval(thefile.read())
thefile.close()

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

previous_word = ""
for index, tag in enumerate(start_tag_list):
    if index == 0:
        terminal = random.choice(tag_word_map[tag])
        previous_word = terminal
    else:
        terminal = random.choice(tag_generator.cfd[previous_word].most_common(1))[0]
        choice = 1
        while terminal not in tag_word_map[tag]:
            terminal = random.choice(tag_generator.cfd[previous_word].most_common(choice))[0]
            choice += 1

        previous_word = terminal

    cfg += tag + " -> " + "'" + terminal + "'" + "\n"

print cfg

grammar = nltk.CFG.fromstring(cfg)

for sentence in generate(grammar):
    title = ' '.join(sentence)
    #print title
    #print (str(textstat.flesch_reading_ease(title)) + ": " + title)

