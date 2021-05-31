from bs4 import BeautifulSoup
import requests

from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

from joblib import load

import spacy
nlp = spacy.load('en_core_web_sm')

import string

from .models import RSS_links

def get_data(rss_link):
    res = requests.get(rss_link)
    soup = BeautifulSoup(res.text, 'xml')

    all_titles = soup.findAll('title')[1:]
    all_descriptions = soup.findAll('description')[1:]
    all_links = soup.findAll('link')[1:]

    all_data_dict = {}

    for i in range(len(all_titles)):
        d_temp = {}
        d_temp['desc'] = all_descriptions[i].contents[0].rstrip().lstrip()
        d_temp['link'] = all_links[i].contents[0].rstrip().lstrip()
        d_temp['sentiment'] = 0

        all_data_dict[all_titles[i].contents[0].rstrip().lstrip()] = d_temp

    return all_data_dict

def get_rss_links_dict():

    # rss_links_dict = {
    #     'na': 'https://www.thehindu.com/news/national/feeder/default.rss',
    #     'in': 'https://www.thehindu.com/news/international/feeder/default.rss',
    #     'op': 'https://www.thehindu.com/opinion/feeder/default.rss',
    #     'sp': 'https://www.thehindu.com/sport/feeder/default.rss',
    #     'bs': 'https://www.thehindu.com/business/feeder/default.rss'
    # }

    all_rss_links = [rss for rss in RSS_links.objects.all().values()]
    all_rss_links_dict = {a['title']: a['url'] for a in all_rss_links}
    return all_rss_links_dict


# MODEL BEGINS FROM HERE
model_jl = load('ml_model/pipeline_for_prod_imdb.joblib')
def text_process_spacy(mess):
    # Check characters to see if they are in punctuation
    nopunc = [char for char in mess if char not in string.punctuation]

    # Join the characters again to form the string.
    nopunc = ''.join(nopunc)
    nopunc = nlp(nopunc)
    
    # Now just remove any stopwords
    return " ".join([word.text for word in nopunc if not word.is_stop])

def predict_sentiment(raw_data={}, process='pos'):
    all_strings = [text_process_spacy(r + ' ' + raw_data[r]['desc']) for r in raw_data]
    
    sentiments = model_jl.predict(all_strings)

    i = 0
    for r in raw_data:
        raw_data[r]['sentiment'] = int(sentiments[i])
        i+=1

    # print(raw_data)
    return raw_data
