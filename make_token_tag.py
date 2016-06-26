# -*- coding: utf-8 -*-
from utils import  myutils
import nltk

tokenized_titles = []
for title in titles:
    tokenized = myutils.tokenize_zh_line(title)
    tokenized_titles.append(tokenized)



# write tokenize to file
tokenized_file = open("data/tokenized", "w")
tokenized_file.write(str(tokenized_titles))
tokenized_file.close()


# taging one thread too slow
# tagged_titles = []
# for title in tokenized_titles:
#     tagged = nltk.pos_tag(title)
#     tagged_titles.append(tagged)


# taging multithread version
tagged_titles = myutils.multi_thread_pool(nltk.pos_tag, tokenized_titles, 8)


# write tags to file
thefile = open('tagged', 'w')
thefile.write(str(tagged_titles))
thefile.close()
