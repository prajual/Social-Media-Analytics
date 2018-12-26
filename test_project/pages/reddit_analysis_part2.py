from ggplot import *
def preprocess(text):
    import string
    import re
    import nltk
    text=text.strip()
    text=re.sub(r'[^\w\s]','',text)
    text=text.lower()
    text= re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE) 
    
    tokens=nltk.word_tokenize(text)
    return (tokens)

def viz_worldcloud(column):
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud
    import itertools
    lst_token=list(itertools.chain.from_iterable(column))
    total_phrase=[phrase.replace(" ","_") for phrase in lst_token if len(lst_token)>1]
    wordcloud = WordCloud(background_color="white", max_words=2000, max_font_size=40, random_state=42).generate(" ".join(total_phrase))
    
    plt.figure()
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    return lst_token
    

def reddit2(user,name):
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
	import itertools
	import nltk
	from wordcloud import WordCloud
	import seaborn as sns
	hdr = {'User-Agent': 'osx:r/relationships.single.result:v1.0 (by /u/<Prajual1391>)'}
	ur = 'https://www.reddit.com/r/{variable}/top/.json?sort=top&t=all'
	url=ur.replace('{variable}',user)
	result = requests.get(url, headers=hdr).json()
	g=pd.DataFrame(result['data']['children'])
	p=list(g['data'])
	reddit_data=pd.DataFrame(p)
	columns_to_keep=['approved_by','author','author_flair_text_color','author_fullname','clicked','can_mod_post','contest_mode','created','domain','downs','edited','gildings','id','is_video','likes','media','media_embed','name','no_follow','num_comments','num_crossposts','num_reports','permalink','pwls','score','selftext','subreddit','suggested_sort','title','ups','url']
	reddit_data=reddit_data[columns_to_keep]
	reddit_data=reddit_data[reddit_data['author']==name]
	different_authors=pd.DataFrame(reddit_data['author'].value_counts())
	names=list(different_authors.index)
	numbers=list(different_authors['author'])
	y = numbers
	plt.title('Number of Posts from the input Authors')
	plt.ylabel('Number of Posts')
	plt.xticks(range(len(y)), names,rotation=40, ha='right')
	plt.bar(range(len(y)),height=y,width=0.75,align='center',alpha=0.8)
	plt.tight_layout()
	plt.show()
	reddit_data['clicked']=reddit_data['clicked'].replace(False,0)
	reddit_data['clicked']=reddit_data['clicked'].replace(True,1)
	reddit_data['edited']=reddit_data['edited'].replace(False,0)
	reddit_data['edited']=reddit_data['edited'].replace(True,1)
	reddit_data['is_video']=reddit_data['is_video'].replace(False,0)
	reddit_data['is_video']=reddit_data['is_video'].replace(True,1)


	ax=sns.barplot(data=reddit_data,x=reddit_data.index,y='clicked')
	ax.set(xlabel='Posts Number', ylabel='Clicked')
	plt.show()
	bx=sns.barplot(data=reddit_data,x=reddit_data.index,y='edited')
	bx.set(xlabel='Posts Number', ylabel='edited')
	plt.show()
	cx=sns.barplot(data=reddit_data,x=reddit_data.index,y='is_video')
	cx.set(xlabel='Posts Number', ylabel='is a Video?')
	plt.show()
	dx=sns.barplot(data=reddit_data,x=reddit_data.index,y='num_comments')
	dx.set(xlabel='Posts Number', ylabel='Number of Comments')
	plt.show()
	ex=sns.barplot(data=reddit_data,x=reddit_data.index,y='num_crossposts')
	ex.set(xlabel='Posts Number', ylabel='Number of Crossposts')
	plt.show()
	fx=sns.barplot(data=reddit_data,x=reddit_data.index,y='num_reports')
	fx.set(xlabel='Posts Number', ylabel='Number of Reports')
	plt.show()
	gx=sns.barplot(data=reddit_data,x=reddit_data.index,y='score')
	gx.set(xlabel='Posts Number', ylabel='Score')
	plt.show()
	hx=sns.barplot(data=reddit_data,x=reddit_data.index,y='ups')
	hx.set(xlabel='Posts Number', ylabel='Ups')
	plt.show()
	reddit_data['preprocess_self']=reddit_data.apply(lambda x:preprocess(x['selftext']),axis=1)
	reddit_data['preprocess_title']=reddit_data.apply(lambda x:preprocess(x['title']),axis=1)
	stopwords_vocabulary=stopwords.words('english')
	reddit_data['stopwords_self']=reddit_data['preprocess_self'].apply(lambda x:[i for i in x if i.lower() not in stopwords_vocabulary])
	punctuations=list(string.punctuation)
	digit=list(string.digits)
	reddit_data['punctuation_self']=reddit_data['stopwords_self'].apply(lambda x:[i for i in x if i not in punctuations])
	reddit_data['digit_self']=reddit_data['punctuation_self'].apply(lambda x: [i for i in x if i[0] not in digit])
	reddit_data['final_self']=reddit_data['digit_self'].apply(lambda x: [i for i in x if len(i) > 1])
	reddit_data['stopwords_title']=reddit_data['preprocess_title'].apply(lambda x:[i for i in x if i.lower() not in stopwords_vocabulary])
	reddit_data['punctuation_title']=reddit_data['stopwords_title'].apply(lambda x:[i for i in x if i not in punctuations])
	reddit_data['digit_title']=reddit_data['punctuation_title'].apply(lambda x: [i for i in x if i[0] not in digit])
	reddit_data['final_title']=reddit_data['digit_title'].apply(lambda x: [i for i in x if len(i) > 1])
	words_posts=viz_worldcloud(reddit_data['final_self'])
	words_title=viz_worldcloud(reddit_data['final_title'])
	reddit_data=reddit_data.set_index('author')
	columns=['name','id','permalink','url','title','selftext']
	reddit_data=reddit_data[columns]
	return (reddit_data)
	
	
	

