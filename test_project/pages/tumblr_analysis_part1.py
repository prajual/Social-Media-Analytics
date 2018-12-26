def tumblr1(blog_name):
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
	blog = pytumblr.TumblrRestClient('jC97cLAMvvK5nZ0g4rDDfBP2TB48XjQlbvV8qV7jgEQAIU4dM4')
	info=blog.blog_info(blog_name)
	avatar=blog.avatar(blog_name)
	client = MongoClient('localhost:27017')
	db = client.tumblr
	collection1=db.information
	collection1.drop()
	collection1.insert_one(info['blog'])
	documents=[]
	for i in collection1.find():
    		try:
        		documents.append(i)
    		except:
        		pass
    
	information=pd.DataFrame(documents)
	information['avatar']=avatar['avatar_url']
	number_of_likes=information.iloc[0]['likes']
	number_of_posts=information.iloc[0]['posts']
	number_of_total_posts=information.iloc[0]['total_posts']
	y = [number_of_likes,number_of_posts,number_of_total_posts]
	plt.title('Statistics')
	plt.ylabel('Statistics Values')
	plt.xticks(range(len(y)), ['likes','posts','total_posts'])
	plt.bar(range(len(y)),height=y,width=0.75,align='center',alpha=0.8)
	plt.show()
	url=information.iloc[0]['url']
	avatar=information.iloc[0]['avatar']
	ask_title=information.iloc[0]['ask_page_title']
	description=information.iloc[0]['description']
	return (url,avatar,ask_title,description)
	

