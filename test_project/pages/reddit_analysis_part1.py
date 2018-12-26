from ggplot import *
from tkinter import *
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
    

def reddit1(name):
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
	url=ur.replace('{variable}',name)
	result = requests.get(url, headers=hdr).json()
	g=pd.DataFrame(result['data']['children'])
	p=list(g['data'])
	reddit_data=pd.DataFrame(p)
	columns_to_keep=['approved_by','author','author_flair_text_color','author_fullname','clicked','can_mod_post','contest_mode','created','domain','downs','edited','gildings','id','is_video','likes','media','media_embed','name','no_follow','num_comments','num_crossposts','num_reports','permalink','pwls','score','selftext','subreddit','suggested_sort','title','ups','url']
	reddit_data=reddit_data[columns_to_keep]
	different_authors=pd.DataFrame(reddit_data['author'].value_counts())
	names=list(different_authors.index)
	numbers=list(different_authors['author'])
	y = numbers
	plt.title('Number of Posts from Different Authors')
	plt.ylabel('Number of Posts')
	plt.xticks(range(len(y)), names,rotation=40, ha='right')
	plt.bar(range(len(y)),height=y,width=0.75,align='center',alpha=0.8)
	plt.tight_layout()
	plt.show()
	reddit_data['clicked']=reddit_data['clicked'].replace(False,0)
	reddit_data['clicked']=reddit_data['clicked'].replace(True,1)
	reddit_data['is_video']=reddit_data['is_video'].replace(False,0)
	reddit_data['is_video']=reddit_data['is_video'].replace(True,1)
	reddit_data['no_follow']=reddit_data['no_follow'].replace(False,0)
	reddit_data['no_follow']=reddit_data['no_follow'].replace(True,1)
	number_of_videos_clicked=sum(reddit_data['clicked'])
	plt.bar("Number of Posts Clicked",height=number_of_videos_clicked,alpha=0.8)
	plt.title('Number of Posts Clicked')
	plt.ylabel('Number of Posts')
	plt.show()
	Domains=pd.DataFrame(reddit_data['domain'].value_counts())
	names=list(Domains.index)
	numbers=list(Domains['domain'])
	y = numbers
	plt.title('Number of Posts with different domains')
	plt.ylabel('Number of Posts')
	plt.xticks(range(len(y)), names)
	plt.bar(range(len(y)),height=y,width=0.75,align='center',alpha=0.8)
	plt.tight_layout()
	plt.show()
	number_of_videos=sum(reddit_data['is_video'])
	plt.bar("Number of Videos",height=number_of_videos,alpha=0.8)
	plt.title("Number of Videos")
	plt.ylabel("Number of posts")
	gids=list(reddit_data['gildings'])
	gids_data=pd.DataFrame(gids)
	ax=sns.barplot(data=reddit_data,y='ups',x=reddit_data.index)
	ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
	ax.set_ylabel('Ups of posts')
	ax.set_xlabel('posts Number')
	ax.set_title('Ups of Posts by different authors')
	plt.show()
	bx=sns.barplot(y=list(gids_data['gid_2']),x=reddit_data.index)
	bx.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
	bx.set_ylabel('Gid_2 values of posts')
	bx.set_xlabel('posts Number')
	bx.set_title('Gid_2 values of posts by different authors')
	plt.show()
	cx=sns.barplot(data=reddit_data,x=reddit_data.index,y='num_comments')
	cx.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
	cx.set_ylabel('Number of comments on posts')
	cx.set_xlabel('posts Number')
	cx.set_title('Number of comments on Posts by different authors')
	plt.show()
	dx=sns.barplot(data=reddit_data,x=reddit_data.index,y='num_crossposts')
	dx.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
	dx.set_ylabel('Number of crossposts on posts')
	dx.set_xlabel('posts Number')
	dx.set_title('Number of crossposts on Posts by different authors')
	plt.show()
	ex=sns.barplot(data=reddit_data,x=reddit_data.index,y='score')
	ex.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
	ex.set_ylabel('Score on posts')
	ex.set_xlabel('posts Number')
	ex.set_title('Score on Posts by different authors')
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
	columns=['permalink','url','title']
	reddit_data=reddit_data[columns]
	return (reddit_data)
		
	
