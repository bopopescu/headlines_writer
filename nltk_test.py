import nltk
from nltk.parse import RecursiveDescentParser
from nltk.parse.generate import generate, demo_grammar
from nltk import CFG


titles = ["14 ways to derp a best friend", "5 ways to shave a cat"] 

processed_titles = []

for title in titles:
    tokenized = nltk.word_tokenize(title)
    tagged = nltk.pos_tag(tokenized)
    processed_titles.append(tagged)

#flatten lists of tagged words
all_tags = [item for sublist in processed_titles for item in sublist]

tag_word_map = {}

for word, tag in all_tags:
    if tag in tag_word_map:
        tag_word_map[tag].append(word)   
    else:
        tag_word_map[tag] = [word]

cfg = "S -> NP VP\n"
cfg += "NP -> VB\n" 
cfg += "VP -> NN\n" 


demo_grammar = """
    S -> NP VP
    NP -> 'derp'
    VP -> 'cat'
    """

for tag, words in tag_word_map.iteritems():
    cfg += tag + ' -> '  
    words = list(set(words))
    for word in words:
        if word != words[-1]: 
            cfg += "'" + word + "'" + ' | '
        else:
            cfg += "'" + word + "'"
    cfg += "\n"

print cfg
grammar1 = nltk.CFG.fromstring(cfg)
for sentence in generate(grammar1):
    print(' '.join(sentence))






