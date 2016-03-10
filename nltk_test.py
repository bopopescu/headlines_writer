import nltk
from textstat.textstat import textstat
from nltk.tokenize import RegexpTokenizer
import random
from nltk.parse.generate import generate
from nltk import CFG
import math
from nltk.corpus import stopwords

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


def comp(tag_sequence, generated_tag_sequence):
    matches = 0
    for index in range(len(tag_sequence)):
        if len(generated_tag_sequence) > index:
            if (tag_sequence[index] == generated_tag_sequence[index]):
                matches += 1
        else:
            break
            
    return matches


match_found = False
while not match_found:
    generated_title = (tag_generator.generate_model(tag_generator.cfd, random.choice(tag_generator.first_words))).lower()

    tokenizer = RegexpTokenizer(r"\w+'?\w+")
    tokenized = tokenizer.tokenize(generated_title)
    last_word = tokenized[-1]
    if(last_word in stopwords.words('english')):
        continue
    if generated_title in tag_generator.titles:
        print "EXACT MATCH"
        continue

    tagged = nltk.pos_tag(tokenized)
    match_cutoff = int(math.ceil(len(tokenized) *.80))

    generated_structure = []
    for word_tag_pair in tagged:
        generated_structure.append(word_tag_pair[1])

    nouns = ["NN", "NNS", "NNP", "NNPS"]

    if(generated_structure[-1] not in nouns):
        print "NON NOUN"
        continue

    for sentence_structure in sentence_structures:
        match_count = comp(sentence_structure, generated_structure)
        if match_count >= match_cutoff:
            match_found = True
            break

print generated_title

