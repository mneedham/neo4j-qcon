from __future__ import print_function
from time import time

import csv
import sys
import os

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF
from collections import defaultdict
from bs4 import BeautifulSoup, NavigableString
from soupselect import select
from sklearn.decomposition import TruncatedSVD

def uri_to_file_name(uri):
    return uri.replace("/", "-")

t0 = time()
sessions = {}
with open("data/sessions.csv", "r") as sessions_file:
    reader = csv.reader(sessions_file, delimiter = ",")
    reader.next() # header
    for row in reader:
        session_id = int(row[0])
        filename = "data/sessions/" + uri_to_file_name(row[4])
        page = open(filename).read()
        soup = BeautifulSoup(page)
        abstract = select(soup, "div.brenham-main-content p")
        if abstract:
            sessions[session_id] = {"abstract" : abstract[0].text, "title": row[3] }
        else:
            abstract = select(soup, "div.pane-content p")
            sessions[session_id] = {"abstract" : abstract[0].text, "title": row[3] }

corpus = []
titles = []
for id, session in sorted(sessions.iteritems(), key=lambda t: int(t[0])):
    corpus.append(session["abstract"])
    titles.append(session["title"])

n_topics = 15
n_top_words = 50
n_features = 6000

# tf = TfidfVectorizer(analyzer='word', ngram_range=(1,3), min_df = 0, stop_words = 'english')
tf = CountVectorizer(analyzer='word', ngram_range=(1,1), min_df = 0, stop_words = 'english')
tfidf_matrix =  tf.fit_transform(corpus)
feature_names = tf.get_feature_names()

import lda
import numpy as np

vocab = feature_names

model = lda.LDA(n_topics=20, n_iter=500, random_state=1)
model.fit(tfidf_matrix)
topic_word = model.topic_word_
n_top_words = 20

with open("data/topics.csv", "w") as file:
    writer = csv.writer(file, delimiter=",")
    writer.writerow(["topicId", "word"])

    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
        for topic_word in topic_words:
            writer.writerow([i, topic_word])
        # print('Topic {}: {}'.format(i, ' '.join(topic_words)))

with open("data/sessions-topics.csv", "w") as file:
    writer = csv.writer(file, delimiter=",")
    writer.writerow(["sessionId", "topicId"])

    doc_topic = model.doc_topic_
    for i in range(0, len(titles)):
        writer.writerow([i, doc_topic[i].argmax()])
        print("{} (top topic: {})".format(titles[i], doc_topic[i].argmax()))

# Fit the NMF model
# print("Fitting the NMF model with n_features=%d..."
#       % (n_features))
# nmf = NMF(n_components=n_topics, random_state=1).fit(tfidf_matrix)
# print("done in %0.3fs." % (time() - t0))
#
# feature_names = tf.get_feature_names()
#
# for topic_idx, topic in enumerate(nmf.components_):
#     print("Topic #%d:" % topic_idx)
#     print(" ".join([feature_names[i]
#                     for i in topic.argsort()[:-n_top_words - 1:-1]]))
#     print()

# with open("data/tfidf_scikit.csv", "w") as file:
#     writer = csv.writer(file, delimiter=",")
#     writer.writerow(["SessionId", "Phrase", "Score"])
#     doc_id = 0
#     for doc in tfidf_matrix.todense():
#         print "Document %d" %(doc_id)
#         word_id = 0
#         for score in doc.tolist()[0]:
#             if score > 0:
#                 word = feature_names[word_id]
#                 writer.writerow([doc_id, word.encode("utf-8"), score])
#             word_id +=1
#         doc_id +=1
