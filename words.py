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

vectorizer = CountVectorizer(analyzer='word', ngram_range=(1,1), min_df = 0, stop_words = 'english')
matrix =  vectorizer.fit_transform(corpus)

feature_names = vectorizer.get_feature_names()

print matrix
