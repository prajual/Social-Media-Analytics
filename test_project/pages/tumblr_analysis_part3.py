def preprocess(text):
    import re
    import nltk
    import string
    text=text.strip()
    text=re.sub(r'[^\w\s]','',text)
    text=text.lower()
    text= re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE) 
    
    tokens=nltk.word_tokenize(text)
    return (tokens)

def viz_worldcloud(column):
    import itertools
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    lst_token=list(itertools.chain.from_iterable(column))
    total_phrase=[phrase.replace(" ","_") for phrase in lst_token if len(lst_token)>1]
    wordcloud = WordCloud(background_color="white", max_words=2000, max_font_size=40, random_state=42).generate(" ".join(total_phrase))
    
    plt.figure()
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    return lst_token


def tumblr3(word,nu):
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
	import pytumblr
	import re
	import nltk
	import itertools
	from wordcloud import WordCloud
	blog = pytumblr.TumblrRestClient('jC97cLAMvvK5nZ0g4rDDfBP2TB48XjQlbvV8qV7jgEQAIU4dM4')
	blog_reblog=blog.tagged(word)
	tag=pd.DataFrame(blog_reblog)
	tag=tag.set_index('date')
	tag['preprocess']=tag.apply(lambda x:preprocess(x['summary']),axis=1)
	stopwords_vocabulary=stopwords.words('english')
	tag['stopwords']=tag['preprocess'].apply(lambda x:[i for i in x if i.lower() not in stopwords_vocabulary])
	punctuations=list(string.punctuation)
	digit=list(string.digits)
	tag['punctuation']=tag['stopwords'].apply(lambda x:[i for i in x if i not in punctuations])
	tag['digit']=tag['punctuation'].apply(lambda x: [i for i in x if i[0] not in digit])
	tag['final']=tag['digit'].apply(lambda x: [i for i in x if len(i) > 1])
	different_bloggers=pd.DataFrame(tag['blog_name'].value_counts())
	names=list(different_bloggers.index)
	numbers=list(different_bloggers['blog_name'])
	y = numbers
	plt.title('Number of posts from Different handles')
	plt.ylabel('Number of Posts')
	plt.xticks(range(len(y)), names,rotation=40, ha='right')
	plt.bar(range(len(y)),height=y,width=0.75,align='center',alpha=0.8)
	plt.tight_layout()
	plt.show()
	blog_data=list(tag['blog'])
	blogger=pd.DataFrame(blog_data)
	blogger=blogger.set_index('name')
	num=int(nu)
	blogger_specified=pd.DataFrame(blogger.index.value_counts())
	blogger=pd.merge(blogger,blogger_specified,how='outer',left_index=True,right_index=True)
	blogger=blogger[blogger['name']==num]
	columns=['description','title','url']
	blogger=blogger[columns]
	
	return  blogger
