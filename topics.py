import csv

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF
from collections import defaultdict
from bs4 import BeautifulSoup, NavigableString
from soupselect import select

def uri_to_file_name(uri):
    return uri.replace("/", "-")

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

# vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1,1), min_df = 0, stop_words = 'english')
vectorizer = CountVectorizer(analyzer='word', ngram_range=(1,1), min_df = 0, stop_words = 'english')
matrix =  vectorizer.fit_transform(corpus)
feature_names = vectorizer.get_feature_names()

import lda
import numpy as np

vocab = feature_names

model = lda.LDA(n_topics=20, n_iter=500, random_state=1)
model.fit(matrix)
topic_word = model.topic_word_
n_top_words = 20

for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
    print('Topic {}: {}'.format(i, ' '.join(topic_words)))

doc_topic = model.doc_topic_
for i in range(0, len(titles)):
    print("{} (top topic: {})".format(titles[i], doc_topic[i].argmax()))
    print(doc_topic[i].argsort()[::-1][:3])

# with open("data/topics.csv", "w") as file:
#     writer = csv.writer(file, delimiter=",")
#     writer.writerow(["topicId", "word"])
#
#     for i, topic_dist in enumerate(topic_word):
#         topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
#         for topic_word in topic_words:
#             writer.writerow([i, topic_word])
#         print('Topic {}: {}'.format(i, ' '.join(topic_words)))
#
# with open("data/sessions-topics.csv", "w") as file:
#     writer = csv.writer(file, delimiter=",")
#     writer.writerow(["sessionId", "topicId"])
#
#     doc_topic = model.doc_topic_
#     for i in range(0, len(titles)):
#         writer.writerow([i, doc_topic[i].argmax()])
#         print("{} (top topic: {})".format(titles[i], doc_topic[i].argmax()))
#         print(doc_topic[i].argsort()[::-1][:3])
