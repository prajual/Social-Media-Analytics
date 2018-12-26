from ggplot import *
def preprocess(text):
    import requests 
    import matplotlib.pyplot as plt
    import json 
    import pandas as pd
    import nltk
    import re
    text=text.strip()
    text=re.sub(r'[^\w\s]','',text)
    text=text.lower()
    text= re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE) 
    
    tokens=nltk.word_tokenize(text)
    return (tokens)

def hashtags(text):
    import requests 
    import matplotlib.pyplot as plt
    import json 
    import pandas as pd
    import nltk
    import re
    hashtags=re.findall(r"#(\w+)", text)
    return (hashtags)

def tag_token(preprocessed_token):
    import requests 
    import matplotlib.pyplot as plt
    import json 
    import pandas as pd
    import nltk
    import re
    pos=nltk.pos_tag(preprocessed_token)
    return (pos)
    
def get_keywords(tagged_tokens,pos='all'): 
    import requests 
    import matplotlib.pyplot as plt
    import json 
    import pandas as pd
    import nltk
    import re
    if(pos == 'all'):        
        lst_pos = ('NN','JJ','VB')    
    elif(pos == 'nouns'):         
        lst_pos = 'NN'    
    elif(pos == 'verbs'):        
        lst_pos = 'VB'     
    elif(pos == 'adjectives'):
        lst_pos = 'JJ'    
    else:        
        lst_pos = ('NN','JJ','VB')     
    
    keywords = [tup[0] for tup in tagged_tokens if tup[1].startswith(lst_pos)]      
    return(keywords) 

def get_noun_phrase(tagged_tokens):
    import requests 
    import matplotlib.pyplot as plt
    import json 
    import pandas as pd
    import nltk
    import re
    
    grammar="NP: {<DT>?<JJ>*<NN>}"
    cp=nltk.RegexpParser(grammar)
    tree=cp.parse(tagged_tokens)
    
    result=[]
    for subtree in tree.subtrees(filter=lambda t:t.label()=='NP'):
        if(len(subtree.leaves())>1): 
            outputs = [tup[0] for tup in subtree.leaves()] 
            outputs=" ".join(outputs)
            result.append(outputs)
            
            
    return result

def data(dataframe):
    import requests 
    import matplotlib.pyplot as plt
    import json 
    import pandas as pd
    import nltk
    import re
    
    dataframe['hashtags']=dataframe.apply(lambda x:hashtags(x['message']),axis=1)
    dataframe['preprocess']=dataframe.apply(lambda x:preprocess(x['message']),axis=1)
    dataframe['tagging']=dataframe.apply(lambda x:tag_token(x['preprocess']),axis=1)
    dataframe['keywords']=dataframe.apply(lambda x:get_keywords(x['tagging'],'all'),axis=1)
    dataframe['noun_phrase']=dataframe.apply(lambda x:get_noun_phrase(x['tagging']),axis=1)
    return dataframe

def viz_worldcloud(column):
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    import datetime
    import itertools
    lst_token=list(itertools.chain.from_iterable(column))
    total_phrase=[phrase.replace(" ","_") for phrase in lst_token if len(lst_token)>1]
    wordcloud = WordCloud(background_color="white", max_words=2000, max_font_size=40, random_state=42).generate(" ".join(total_phrase))
    
    plt.figure()
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    return lst_token

def peak(df,criterium):
    import requests 
    import matplotlib.pyplot as plt
    import json 
    import pandas as pd
    import nltk
    import datetime
    import re
    start_week=(df[criterium].idxmax()-datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    end_week=df[criterium].idxmax().strftime('%Y-%m-%d')
    return (start_week,end_week) 

def facebook3(access):
	import requests 
	import matplotlib.pyplot as plt
	import json 
	import pandas as pd
	import nltk
	import re
	from wordcloud import WordCloud
	import datetime
	import seaborn as sns
	from nltk.sentiment.vader import SentimentIntensityAnalyzer
	sentiment=SentimentIntensityAnalyzer()
	import itertools
	params = {'access_token':access}
	from pymongo import MongoClient
	page_url = 'https://graph.facebook.com/v2.8/me/feed?fields=id,message,reactions,shares,from,caption,created_time,likes.summary(true)'
	comments_url = 'https://graph.facebook.com/v2.8/{post_id}/comments?filter=stream&limit=100'
	client = MongoClient('localhost:27017')
	db = client.facebook
	collection_posts=db.posts
	collection_comments=db.comments
	collection_posts.drop()
	collection_comments.drop()
	posts = requests.get(page_url, params = params).json()
	while True:
    		try:
        		for element in posts['data']:
            			collection_posts.insert_one(element)
            			this_comment_url = comments_url.replace("{post_id}",element['id'])
            			comments=requests.get(this_comment_url,params=params).json()
            			while ('paging' in comments and 'cursors' in comments['paging'] and 'after' in comments['paging']['cursors']): 
                			for comment in comments['data']:
                    				comment['post_id']=element['id']
                    				collection_comments.insert_one(comment) 
                			comments = requests.get(this_comment_url + '&after=' + comments['paging']['cursors']['after'], params = params).json()  
        		posts=requests.get(posts['paging']['next']).json()   
    		except Exception as e:       
        		break 
	posts_data=[]
	comments_data=[]
	for doc in collection_posts.find({}):
    		try:
        		posts_data.append((doc['message'],doc['created_time'],doc['likes']['summary']['total_count'],doc['shares']['count'],doc['id']))
    		except:
        		pass

	for comment in collection_comments.find({}):
		try:
        		comments_data.append((comment['message'],comment['created_time'],comment['post_id']))
		except:
        		pass

	df_posts=pd.DataFrame(posts_data)
	df_comments=pd.DataFrame(comments_data)
	df_posts.columns=['message','Created Time','Number of Likes','Shares','post_id']
	df_comments.columns=['message','Created Time','post_id']
	pos=data(df_posts)
	com=data(df_comments)
	fre=viz_worldcloud(pos['keywords'])
	pos['tags']=pd.DataFrame(fre)
	plo=pos.groupby(['tags']).sum()
	plo['poo']=plo.index
	ax=sns.barplot(data=plo,x='poo',y='Number of Likes',palette='rainbow')
	ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
	ax.set_title('Popular tags and Number of Likes')
	ax.set_ylabel('Number of Likes')
	plt.show()
	pos['time']=pos['Created Time'].apply(pd.to_datetime)
	pos=pos.set_index(['time'])
	com['time']=com['Created Time'].apply(pd.to_datetime)
	com=com.set_index(['time'])
	pos['sentiment']=pos['message'].apply(lambda x: sentiment.polarity_scores(x)['compound'])
	com['sentiment']=com['message'].apply(lambda x: sentiment.polarity_scores(x)['compound'])
	dx=pos.resample('W').mean()
	pos=pos.reset_index()
	p = ggplot(pos, aes(x='time', y = 'Number of Likes')) + geom_line()
	p=p+xlab('Timeline')+ylab('Number of Likes')+ggtitle('When did you got the Likes')
	print(p)
	(star,end)=peak(dx,'Number of Likes')
	print("start date:" + star)
	print("end date:"+ end)
	max_number_of_likes=pos[pos['Number of Likes']==pos['Number of Likes'].max()]
	return (max_number_of_likes['message']) 
	


