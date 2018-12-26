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
    

def reddit3(user,nu):
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
	num=int(nu)
	columns_to_keep=['approved_by','author','author_flair_text_color','author_fullname','clicked','can_mod_post','contest_mode','created','domain','downs','edited','gildings','id','is_video','likes','media','media_embed','name','no_follow','num_comments','num_crossposts','num_reports','permalink','pwls','score','selftext','subreddit','suggested_sort','title','ups','url']
	reddit_data=reddit_data[columns_to_keep]
	different_authors=pd.DataFrame(reddit_data['author'].value_counts())
	reddit_data=reddit_data.set_index('author')
	reddit=pd.merge(different_authors,reddit_data,how='outer',left_index=True,right_index=True)
	reddit=reddit[reddit['author']==num]
	authors=pd.DataFrame(reddit.index.value_counts())
	names=list(authors.index)
	numbers=list(authors[0])
	y = numbers
	plt.title('Number of posts from Different handles')
	plt.ylabel('Number of Posts')
	plt.xticks(range(len(y)), names,rotation=40, ha='right')
	plt.bar(range(len(y)),height=y,width=0.75,align='center',alpha=0.8)
	plt.tight_layout()
	plt.show()
	reddit['clicked']=reddit['clicked'].replace(False,0)
	reddit['clicked']=reddit['clicked'].replace(True,1)
	reddit['is_video']=reddit['is_video'].replace(False,0)
	reddit['is_video']=reddit['is_video'].replace(True,1)
	reddit['no_follow']=reddit['no_follow'].replace(False,0)
	reddit['no_follow']=reddit['no_follow'].replace(True,1)
	redd=reddit.groupby(by=reddit.index).sum()
	ax=sns.barplot(data=redd,y='clicked',x=redd.index)
	ax.set_ylabel('Number of Posts Clicked')
	plt.show()
	bx=sns.barplot(data=redd,y='is_video',x=redd.index)
	bx.set_ylabel('Number of Videos')
	bx.set_title('Videos by authors')
	plt.show()
	cx=sns.barplot(data=redd,y='no_follow',x=redd.index)
	cx.set_ylabel('Number of followers')
	cx.set_title('Followers of different authors')
	plt.show()
	red=reddit.reset_index()
	dx=sns.barplot(data=red,y='score',x=red.index,hue='index',palette='rainbow')
	dx.set_ylabel('Score of Authors')
	dx.set_title('Score of different posts by different authors')
	dx.legend(loc=1)
	plt.show()
	ex=sns.barplot(data=red,y='ups',x=red.index,hue='index')
	ex.set_ylabel('Ups of Authors')
	ex.set_title('Ups of different posts by different authors')
	ex.legend(loc=1)
	plt.show()
	fx=sns.barplot(data=red,y='num_comments',x=red.index,hue='index')
	fx.set_ylabel('Comments on posts')
	fx.set_title('Comments of different posts by different authors')
	fx.legend(loc=1)
	plt.show()
	gx=sns.barplot(data=red,y='num_crossposts',x=red.index,hue='index',palette='rainbow')
	gx.set_ylabel('Number of crossposts')
	gx.set_title('Number of Cross posts by different authors')
	gx.legend(loc=1)
	plt.show()
	hx=sns.barplot(data=red,y='num_reports',x=red.index,hue='index',palette='rainbow')
	hx.set_ylabel('Number of reports')
	hx.set_title('Number of reports by different authors')
	hx.legend(loc=1)
	plt.show()
	reddit['preprocess_self']=reddit.apply(lambda x:preprocess(x['selftext']),axis=1)
	reddit['preprocess_title']=reddit.apply(lambda x:preprocess(x['title']),axis=1)
	stopwords_vocabulary=stopwords.words('english')
	reddit['stopwords_self']=reddit['preprocess_self'].apply(lambda x:[i for i in x if i.lower() not in stopwords_vocabulary])
	punctuations=list(string.punctuation)
	digit=list(string.digits)
	reddit['punctuation_self']=reddit['stopwords_self'].apply(lambda x:[i for i in x if i not in punctuations])
	reddit['digit_self']=reddit['punctuation_self'].apply(lambda x: [i for i in x if i[0] not in digit])
	reddit['final_self']=reddit['digit_self'].apply(lambda x: [i for i in x if len(i) > 1])
	reddit['stopwords_title']=reddit['preprocess_title'].apply(lambda x:[i for i in x if i.lower() not in stopwords_vocabulary])
	reddit['punctuation_title']=reddit['stopwords_title'].apply(lambda x:[i for i in x if i not in punctuations])
	reddit['digit_title']=reddit['punctuation_title'].apply(lambda x: [i for i in x if i[0] not in digit])
	reddit['final_title']=reddit['digit_title'].apply(lambda x: [i for i in x if len(i) > 1])
	words_posts=viz_worldcloud(reddit['final_self'])
	words_title=viz_worldcloud(reddit['final_title'])
	columns=['permalink','url','title']
	reddit=reddit[columns]
	return reddit
	
	
