from ggplot import *
def preprocess(text):
    import re
    import nltk
    text=text.strip()
    text=re.sub(r'[^\w\s]','',text)
    text=text.lower()
    text= re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE) 
    
    tokens=nltk.word_tokenize(text)
    return (tokens)

def print_verbatims(df,keyword):
    import string
    import itertools
    doc=[]
    verbatims = df[df['text'].str.contains(keyword)] 
    for i,item in verbatims.head().iterrows():
        doc.append(item['text'])
    return (doc)

def twitter3(q):
	import requests 
	from requests_oauthlib import OAuth1
	import json
	from urllib.parse import urlparse
	import json
	from pandas.io.json import json_normalize
	from pymongo import MongoClient
	import pandas as pd
	import numpy as np
	import matplotlib.pyplot as plt
	import seaborn as sns
	from bs4 import BeautifulSoup
	from nltk.tokenize import TweetTokenizer
	from nltk.corpus import stopwords
	import string
	import datetime
	import nltk
	import re
	from nltk.sentiment.vader import SentimentIntensityAnalyzer
	from wordcloud import WordCloud
	import itertools
	params={'app_key':'bYiDrEKxTIVOrDOKlSFfCNTum',
        'app_secret':'XIC6hdq6ARrstADQpIv4HugEca0iWFQ9C6d0kRRol3TtOv976e',
        'oauth_token':'1068456441634152448-8kjkT79Y1f7KiWFMaoexRRzJ9fPiyW',
        'secret_oauth_token':'keaC5qyV9y5k3tQdHPGxBwDFkeR7Kj1MiYlWB7SfsbVlt'
       }
	auth=OAuth1(params['app_key'],
             params['app_secret'],
             params['oauth_token'],
             params['secret_oauth_token']
           )
	url='https://api.twitter.com/1.1/search/tweets.json'
	pms={'q':q,'count': 100,'lang': 'en','result_type':'recent'}
	pages_counter=0
	pages_checked=100
	client=MongoClient('mongodb://localhost:27017/')
	db=client.twitter
	collection=db.tweets
	collection.drop()
	while pages_counter<pages_checked :
		try:
    			pages_counter=pages_counter+1
    			results = requests.get(url,params=pms, auth=auth)
    			tweets=results.json()
    			collection.insert_many(tweets['statuses'])
		except Exception as e:
			break
	documents=[]
	for i in collection.find():
    		try:
        	   documents.append(i)
    		except:
        	   pass
	df=pd.DataFrame(documents)
	df['preprocess']=df.apply(lambda x:preprocess(x['text']),axis=1)
	df['time']=df['created_at'].apply(pd.to_datetime)
	df=df.set_index(['time'])
	df['tokens']=df['text'].apply(TweetTokenizer().tokenize)
	stopwords_vocabulary=stopwords.words('english')
	df['stopwords']=df['tokens'].apply(lambda x:[i for i in x if i.lower() not in stopwords_vocabulary])
	punctuations=list(string.punctuation)
	digit=list(string.digits)
	df['punctuation']=df['stopwords'].apply(lambda x:[i for i in x if i not in punctuations])
	df['digit']=df['punctuation'].apply(lambda x: [i for i in x if i[0] not in digit])
	df['final']=df['digit'].apply(lambda x: [i for i in x if len(i) > 1])
	sentiment=SentimentIntensityAnalyzer()
	df['sentiment']=df['text'].apply(lambda x: sentiment.polarity_scores(x)['compound'])
	df_pos=df[df['sentiment']>0]
	df_neg=df[df['sentiment']<0]
	df_neu=df[df['sentiment']==0]
	positive_response=print_verbatims(df_pos,'dominoes')
	negative_response=print_verbatims(df_neg,'dominoes')
	neutral_response=print_verbatims(df_neu,'dominoes')
	return (positive_response,negative_response,neutral_response)
	
	
	
	

