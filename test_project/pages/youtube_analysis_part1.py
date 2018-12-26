from ggplot import *
def youtube_search(q, max_results=50,order="relevance", token=None, location=None, location_radius=None):
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

def youtube1(keyword):
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
	from nltk.sentiment.vader import SentimentIntensityAnalyzer
	sentiment=SentimentIntensityAnalyzer()
	from wordcloud import WordCloud
	import itertools
	data = grab_videos(keyword)
	youtube_data=pd.DataFrame(data)
	youtube_data['time']=youtube_data['created'].apply(pd.to_datetime)
	youtube_data=youtube_data.set_index(['time'])
	different_channels=pd.DataFrame(youtube_data['ChannelTitle'].value_counts())
	names=list(different_channels.index)
	numbers=list(different_channels['ChannelTitle'])
	y = numbers
	width = 50
	height = 12
	plt.title('Number of Videos from Different handles')
	plt.ylabel('Number of Videos')
	plt.xticks(range(len(y)), names,rotation=40, ha='right')
	plt.bar(range(len(y)),height=y,width=0.75,align='center',alpha=0.8)
	plt.rcParams['figure.figsize']=[20,40]
	plt.show()
	youtube_data['sentiment']=youtube_data['description'].apply(lambda x: sentiment.polarity_scores(x)['compound'])
	youtube_data=youtube_data.reset_index()
	p = ggplot(youtube_data, aes(x='time', y = 'sentiment')) + geom_line()
	p=p+xlab('Timeline')+ylab('Level of Sentiment')+ggtitle('What was the level of sentiments at different videos')
	print(p)
	respo="Graphs are shown about the videos from different handles"
	return respo
	
