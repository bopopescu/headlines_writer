# -*- coding: utf-8 -*-
zh_title_path = "data/crawled_titles-00001"

#myutils.set_ipython_encoding_utf8()

# load title from file
fd = open(zh_title_path)
titles = [ title.strip() for title in fd.readlines() ]

# remove duplicated title
titles = list(set(titles))

# filted " " title
titles = [title for title in titles if title ]
