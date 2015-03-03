import csv
import requests
from bs4 import BeautifulSoup
from soupselect import select

def uri_to_file_name(uri):
    return uri.replace("/", "-")

with open("data/sessions.csv", "r") as sessions_file:
    reader = csv.reader(sessions_file, delimiter = ",")
    reader.next()
    for row in reader:
        filename = "data/sessions/%s" %(uri_to_file_name(row[3]))
        print filename

        with open(filename, 'wb') as handle:
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            response = requests.get("http://qconlondon.com/" + row[3], headers = headers)
            if response.ok:
                for block in response.iter_content(1024):
                    if not block:
                        break

                    handle.write(block)
