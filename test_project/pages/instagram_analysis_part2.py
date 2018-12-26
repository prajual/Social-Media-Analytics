from ggplot import *
def preprocess(text):
    import re
    import string
    import nltk
    text=text.strip()
    text=re.sub(r'[^\w\s]','',text)
    text=text.lower()
    text= re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE) 
    
    tokens=nltk.word_tokenize(text)
    return (tokens)

def viz_worldcloud(column):
    import itertools
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud
    lst_token=list(itertools.chain.from_iterable(column))
    total_phrase=[phrase.replace(" ","_") for phrase in lst_token if len(lst_token)>1]
    wordcloud = WordCloud(background_color="white", max_words=2000, max_font_size=40, random_state=42).generate(" ".join(total_phrase))
    
    plt.figure()
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    return lst_token
    
def instagram2(access):
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
	import re
	import itertools
	from wordcloud import WordCloud
	import nltk
	import pandas as pd 
	params={'access_token': access}
	url='https://api.instagram.com/v1/users/self'
	result=requests.get(url,params=params).json()
	data=pd.DataFrame(result)
	insta_data=pd.DataFrame(data['data'])
	insta_data=insta_data.T
	count=pd.DataFrame(list(insta_data['counts']))
	followers=count.iloc[0]['followed_by']
	follows=count.iloc[0]['follows']
	posts=count.iloc[0]['media']
	y=[followers,follows,posts]
	names=list(['followers', 'follows' ,'posts'])
	plt.title('Number of followers, follows, posts of the user')
	plt.ylabel('Statistics Value')
	plt.xticks(range(len(y)), names)
	plt.bar(range(len(y)),height=y,width=0.75,align='center',alpha=0.8)
	plt.show()
	respo="Graph for the number of followers, follows and posts of the user is shown"
	return respo

	
