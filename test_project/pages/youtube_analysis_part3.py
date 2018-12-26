def youtube_search(q, max_results=50,order="relevance", token=None, location=None, location_radius=None):
  from apiclient.discovery import build
  from apiclient.errors import HttpError
  from oauth2client.tools import argparser

  DEVELOPER_KEY = "AIzaSyAi2j1feg1vva_Pk7O7_QK5pVnK8-O3FRw"
  YOUTUBE_API_SERVICE_NAME = "youtube"
  YOUTUBE_API_VERSION = "v3"

  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  search_response = youtube.search().list(
    q=q,
    type="video",
    pageToken=token,
    order = order,
    part="id,snippet",
    maxResults=max_results,
    location=location,
    locationRadius=location_radius

  ).execute()



  videos = []

  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos.append(search_result)
  try:
      nexttok = search_response["nextPageToken"]
      return(nexttok, videos)
  except Exception as e:
      nexttok = "last_page"
      return(nexttok, videos)


def geo_query(video_id):
    from apiclient.discovery import build
    from apiclient.errors import HttpError
    from oauth2client.tools import argparser

    DEVELOPER_KEY = "AIzaSyAi2j1feg1vva_Pk7O7_QK5pVnK8-O3FRw"
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    video_response = youtube.videos().list(
        id=video_id,
        part='snippet, recordingDetails, statistics'

    ).execute()

    return video_response



def grab_videos(keyword, token=None):
    video_dict = {'etag':[],'videoID':[],'created':[],'channel':[],'title':[],'description':[],'url':[],'ChannelTitle':[]}
    res = youtube_search(keyword)
    token = res[0]
    videos = res[1]
    for vid in videos:
        video_dict['etag'].append(vid['etag'])
        video_dict['videoID'].append(vid['id']['videoId'])
        video_dict['created'].append(vid['snippet']['publishedAt'])
        video_dict['channel'].append(vid['snippet']['channelId'])
        video_dict['title'].append(vid['snippet']['title'])
        video_dict['description'].append(vid['snippet']['description'])
        video_dict['ChannelTitle'].append(vid['snippet']['channelTitle'])
        video_dict['url'].append(vid['snippet']['thumbnails']['default']['url'])
    return video_dict 

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

def youtube3(keyword,nu):
	import sys
	import json
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
	import nltk
	from wordcloud import WordCloud
	import itertools
	num=int(nu)
	data = grab_videos(keyword)
	youtube_data=pd.DataFrame(data)
	youtube_data['time']=youtube_data['created'].apply(pd.to_datetime)
	youtube_data=youtube_data.set_index(['ChannelTitle'])
	channel_names=pd.DataFrame(youtube_data.index.value_counts())
	youtube_data=pd.merge(channel_names,youtube_data,how='outer',left_index=True,right_index=True)
	youtube_data=youtube_data[youtube_data['ChannelTitle']==num]
	columns=['description','title','url']
	youtube_data=youtube_data[columns]
	youtube_data['preprocess_des']=youtube_data.apply(lambda x:preprocess(x['description']),axis=1)
	stopwords_vocabulary=stopwords.words('english')
	youtube_data['stopwords_des']=youtube_data['preprocess_des'].apply(lambda x:[i for i in x if i.lower() not in stopwords_vocabulary])
	punctuations=list(string.punctuation)
	digit=list(string.digits)
	youtube_data['punctuation_des']=youtube_data['stopwords_des'].apply(lambda x:[i for i in x if i not in punctuations])
	youtube_data['digit_des']=youtube_data['punctuation_des'].apply(lambda x: [i for i in x if i[0] not in digit])
	youtube_data['final_des']=youtube_data['digit_des'].apply(lambda x: [i for i in x if len(i) > 1])
	youtube_data['preprocess_tit']=youtube_data.apply(lambda x:preprocess(x['title']),axis=1)
	youtube_data['stopwords_tit']=youtube_data['preprocess_tit'].apply(lambda x:[i for i in x if i.lower() not in stopwords_vocabulary])
	youtube_data['punctuation_tit']=youtube_data['stopwords_tit'].apply(lambda x:[i for i in x if i not in punctuations])
	youtube_data['digit_tit']=youtube_data['punctuation_tit'].apply(lambda x: [i for i in x if i[0] not in digit])
	youtube_data['final_tit']=youtube_data['digit_tit'].apply(lambda x: [i for i in x if len(i) > 1])
	popular_title=viz_worldcloud(youtube_data['final_tit'])
	popular_des=viz_worldcloud(youtube_data['final_des'])
	return youtube_data
