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
    
def instagram1(access):
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
	params={'access_token':access}
	url='https://api.instagram.com/v1/users/self'
	result=requests.get(url,params=params).json()
	data=pd.DataFrame(result)
	insta_data=pd.DataFrame(data['data'])
	insta_data=insta_data.T
	insta_data['preprocess_des']=insta_data.apply(lambda x:preprocess(x['bio']),axis=1)
	stopwords_vocabulary=stopwords.words('english')
	insta_data['stopwords_des']=insta_data['preprocess_des'].apply(lambda x:[i for i in x if i.lower() not in stopwords_vocabulary])
	punctuations=list(string.punctuation)
	digit=list(string.digits)
	insta_data['punctuation_des']=insta_data['stopwords_des'].apply(lambda x:[i for i in x if i not in punctuations])
	insta_data['digit_des']=insta_data['punctuation_des'].apply(lambda x: [i for i in x if i[0] not in digit])
	insta_data['final_des']=insta_data['digit_des'].apply(lambda x: [i for i in x if len(i) > 1])
	pop_bio=viz_worldcloud(insta_data['final_des'])
	biography=insta_data.iloc[0]['bio']
	name=insta_data.iloc[0]['full_name']
	picture=insta_data.iloc[0]['profile_picture']
	web=insta_data.iloc[0]['website']
	return (biography,name,picture,web)

	
