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

def tumblr4(blog_name):
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
	blog_posts=blog.posts(blog_name)
	posts=pd.DataFrame(blog_posts['posts'])
	posts=posts.set_index('date')
	posts['preprocess']=posts.apply(lambda x:preprocess(x['summary']),axis=1)
	stopwords_vocabulary=stopwords.words('english')
	posts['stopwords']=posts['preprocess'].apply(lambda x:[i for i in x if i.lower() not in stopwords_vocabulary])
	punctuations=list(string.punctuation)
	digit=list(string.digits)
	posts['punctuation']=posts['stopwords'].apply(lambda x:[i for i in x if i not in punctuations])
	posts['digit']=posts['punctuation'].apply(lambda x: [i for i in x if i[0] not in digit])
	posts['final']=posts['digit'].apply(lambda x: [i for i in x if len(i) > 1])
	popular_words=viz_worldcloud(posts['final'])
	popular_tags=viz_worldcloud(posts['tags'])
	different_mediums=pd.DataFrame(posts['type'].value_counts())
	mediums=list(different_mediums.index)
	number=list(different_mediums['type'])
	y = number
	plt.title('Number of posts from Different mediums')
	plt.ylabel('Number of Posts')
	plt.xticks(range(len(y)), mediums, ha='center')
	plt.bar(range(len(y)),height=y,width=0.75,align='center',alpha=0.8)
	plt.tight_layout()
	plt.show()
	return (popular_words,popular_tags)

