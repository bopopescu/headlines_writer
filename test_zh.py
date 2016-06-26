# -*- coding: utf-8 -*-
import nltk, random, math, re, itertools
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from utils import  myutils
from nltk.tokenize import RegexpTokenizer
import re
import jieba
import corpus_data
#myutils.set_ipython_encoding_utf8()


# tokenize
def tokenize_zh_line(zh_line, method='jieba'):
    """
    zh_line:
    Chinese string line

    method:
    tokenize method , default using jieba

    Returns:
    token Chinese word list
    """

    try:
        zh_line = zh_line.decode('utf8')
        zh_line = zh_line.strip()
        zh_line = " ".join(re.findall(ur'[\u4e00-\u9fff\w\_]+', zh_line))

        tokenized_list = jieba.cut(zh_line, cut_all=False)

        res = [ word for word in tokenized_list if word != ' ' ]


        return res

    except AttributeError, attr:
        print zh_line
        return []

tokenized_titles = []
for title in titles:
    tokenized = tokenize_zh_line(title)
    tokenized_titles.append(tokenized)



# write tokenize to file
tokenized_file = open("data/tokenized", "w")
tokenized_file.write(str(tokenized_titles))
tokenized_file.close()


# taging
tagged_titles = []
for title in tokenized_titles:
    tagged = nltk.pos_tag(title)
    tagged_titles.append(tagged)


# taging multithread version
tagged_titles = myutils.multi_thread_pool(nltk.pos_tag, tokenized_titles, 8)


# write tags to file
thefile = open('tagged', 'w')
thefile.write(str(tagged_titles))
thefile.close()


class TitleGenerator:

    #Load tokens and tags from file
    thefile = open('data/tokenized', 'r')
    tokenized_titles = eval(thefile.read())
    thefile.close()

    thefile = open('data/tagged', 'r')
    tagged_titles = eval(thefile.read())
    thefile.close()

    def __init__(self):
        titles = corpus_data.titles
        #choose random slice of 100 titles from dataset
        self.rand = random.randint(0, len(titles) - 100) 

        self.titles = titles[self.rand:self.rand+100]
        self.tokenized_titles_slice = self.tokenized_titles[self.rand:self.rand+100]
        self.tagged_titles_slice = self.tagged_titles[self.rand:self.rand+100]
        self.set_title_range()

        #generate required stats for generation model
        self.bigrams = self.build_bigrams()
        self.freq_dist = self.build_freq_dist()

        #generate required stats for title heuristics
        self.title_pos_structures = self.build_title_pos_structures()

    #compute range of title sizes from random 100 slice
    def set_title_range(self):
        self.min_title_length = 5
        self.max_title_length = 5
        for title in self.titles:
            length = len(title.split())

            if length > self.max_title_length:
                self.max_title_length = length

            if length < self.min_title_length:
                self.min_title_length = length

    def build_freq_dist(self):
        flat_all_bigrams = list(itertools.chain(*self.bigrams))
        return nltk.ConditionalFreqDist(flat_all_bigrams) 

    def build_bigrams(self):
        bigrams = []
        for title in self.tokenized_titles_slice:
            bigrams.append(nltk.bigrams(title))
        return bigrams

    def first_words_list(self):
        first_words = []
        for title in self.tokenized_titles_slice:
            first_words.append(title[0])
        return first_words

    def build_title(self):
        word = random.choice(self.first_words_list()) #choose random seed word from all starting words
        title_length = random.randint(self.min_title_length, self.max_title_length)  #choose random length in range
        generated_title = word + ' '

        for i in range(title_length):
            if (self.freq_dist[word]):
                word = random.choice(self.freq_dist[word].most_common(3))[0]
                generated_title += word + ' '
            else:
                break

        return generated_title.lower()

    def build_title_pos_structures(self):
        sentence_structures = []
        for word_tag_pair in self.tagged_titles:
            temp = []
            for pair in word_tag_pair:
                temp.append(pair[1])
            sentence_structures.append(temp)

        return sentence_structures

    def compare_readability(self,title_pos_structure, generated_title_pos_structure):

        #iterate over real POS tagged titles checking for similarity to generated title
        readability = 0
        for index in range(len(title_pos_structure)):
            if len(generated_title_pos_structure) > index:
                if (title_pos_structure[index] == generated_title_pos_structure[index]):
                    readability += 1
            else:
                break

        return readability

    def generate_title(self):
        match_found = False

        while not match_found:
            generated_title = self.build_title()

            #tokenize and tag generated title
            tokenized = tokenize_zh_line(generated_title)
            last_word = tokenized[-1]
            tagged = nltk.pos_tag(tokenized)


            #disallow title to end in stopword
            stopwords = open('data/stop-words/zh_cn.txt')
            stopwords_list = [ word.decode('utf-8').strip() for word in stopwords.readlines() ]
            if(last_word in stopwords_list):
                continue

            #disallow exact duplicates of existing titles
            if generated_title in " ".join(corpus_data.titles):
                continue

            #require a certain title length
            if len(generated_title.split()) < self.min_title_length:
                continue

            #disallow ending on certain types of words
            generated_structure = []
            for word_tag_pair in tagged:
                generated_structure.append(word_tag_pair[1])

            not_aloud = ["JJ", "CC", "CD", "DT", "JJS", "JJR", "TO", "IN", "LS", "MD", "PDT", "POS",
                        "PP", "PPS", "SYM", "UH", "VBD", "VBG", "VBN", "VBP", "VBZ", "WDT", "WP",
                        "WPS", "WRB"]

            if(generated_structure[-1] in not_aloud):
                continue

            #compute 80% match in pos tags
            match_cutoff = int(math.ceil(len(tokenized) *.80))

            #check if satisfies readability threshold
            for sentence_structure in self.title_pos_structures:
                match_count = self.compare_readability(sentence_structure, generated_structure)
                if match_count >= match_cutoff:
                    match_found = True
                    break

        return generated_title

