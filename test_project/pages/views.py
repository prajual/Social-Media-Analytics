from django.http import HttpResponse
from .models import Question
from django.template import loader
import webbrowser
from django.views.generic import TemplateView
from .facebook_analysis_part1 import facebook1
from .facebook_analysis_part2 import facebook2
from .facebook_analysis_part3 import facebook3
from .facebook_analysis_part4 import facebook4
from .twitter_analysis_part1 import twitter1
from .twitter_analysis_part2 import twitter2
from .twitter_analysis_part3 import twitter3
from .tumblr_analysis_part1 import tumblr1
from .tumblr_analysis_part2 import tumblr2
from .tumblr_analysis_part3 import tumblr3
from .tumblr_analysis_part4 import tumblr4
from .tumblr_analysis_part5 import tumblr5
from .youtube_analysis_part1 import youtube1
from .youtube_analysis_part2 import youtube2
from .youtube_analysis_part3 import youtube3	
from .instagram_analysis_part1 import instagram1	
from .instagram_analysis_part2 import instagram2
from .reddit_analysis_part1 import reddit1
from .reddit_analysis_part2 import reddit2
from .reddit_analysis_part3 import reddit3

class AboutPageView(TemplateView):
	template_name='form.html'
class FacebookGenerator(TemplateView):
	template_name='facebook.html'
class InstagramGenerator(TemplateView):
	template_name='Instagram.html'

def user(request):
	if request.method=='POST':
		APP_ID=request.POST['App_id']
		url="https://developers.facebook.com/tools/explorer/"+APP_ID
		webbrowser.open(url,new=2)
		return HttpResponse("Close this tab it is of no use.")
	else:
		return HttpResponse("Invalid APP_ID")
def user1(request):
	if request.method=='POST':
		CLIENT=request.POST['App_id']
		url="https://api.instagram.com/oauth/authorize/?client_id="+CLIENT+"&redirect_uri=https://www.google.com&response_type=token"
		webbrowser.open(url,new=2)
		return HttpResponse("Close this tab it is of no use.")
	else:
		return HttpResponse("Invalid APP_ID")


def fac1(request):
	if request.method=='POST':
		access=request.POST['access']
		[pop_posts,pop_comment]=facebook1(access)
		response1="Popular words in posts of the user are: %s."
		response2="Popular words in comments of the user are: %s."
		return HttpResponse(response1 % pop_posts + "<br>" + response2 % pop_comment)
	else:
		return HttpResponse("Please click the Button otherwise you will not get nothing")

def fac2(request):
	if request.method=='POST':
		access=request.POST['access']
		pop_in_post=request.POST['word']
		pop_in_comment=request.POST['comment']
		[post_with_word,comment_with_word]=facebook2(access,pop_in_post,pop_in_comment)
		response1="Posts with the input word: %s."
		response2="Comments with the input word: %s."
		return HttpResponse(response1 % post_with_word + "<br>" + response2 % comment_with_word)
	else:
		return HttpResponse("Please click the Button otherwise you will not get nothing")

def fac3(request):
	if request.method=='POST':
		access=request.POST['access']
		message=facebook3(access)
		response="Post with maximum number of Likes: %s."
		return HttpResponse(response % message)
	else:
		return HttpResponse("Please click the Button otherwise you will not get nothing")

def fac4(request):
	if request.method=='POST':
		access=request.POST['access']
		[message,pos_post,neg_post,neg_comment,pos_comment]=facebook4(access)
		response1="Post with maximum number of Shares: %s."
		response2="Post with the most positive sentiment: %s."
		response3="Post with the most negative sentimnent: %s."
		response4="Most Positive Comment: %s."
		response5="MOst Negative Comment: %s."
		return HttpResponse(response1 % message + "<br>" + response2 % pos_post + "<br>" + response3 % neg_post + "<br>" + response4 % pos_comment + "<br>" + response5 % neg_comment)
	else:
		return HttpResponse("Please click the Button otherwise you will not get nothing")

def tw1(request):
	if request.method=='POST':
		q=request.POST['name']
		return HttpResponse(twitter1(q))
	else:
		return HttpResponse("Please click the Button otherwise you will not get nothing")

def tw2(request):
	if request.method=='POST':
		q=request.POST['name']
		[most_positive,most_negative]=twitter2(q)
		response1="Tweet with most positive sentiment is: %s."
		response2="Tweet with most negative sentiment is: %s."
		return HttpResponse(response1 % most_positive + "<br>" + response2 % most_negative)
	else:
		return HttpResponse("Please click the Button otherwise you will not get nothing")

def tw3(request):
	if request.method=='POST':
		q=request.POST['name']
		[post_positive,post_negative,post_neutral]=twitter3(q)
		response1="Tweets with positive sentiments are: %s."
		response2="Tweets with negative sentiments are: %s."
		response3="Tweets with neutral sentiments are: %s."
		return HttpResponse(response1 % post_positive + "<br>" + response2 % post_negative + "<br>" + response3 % post_neutral)
	else:
		return HttpResponse("Please click the Button otherwise you will not get nothing")

def tum1(request):
	if request.method=='POST':
		blog_name=request.POST['name']
		[url,avatar,ask_title,description]=tumblr1(blog_name)
		response1="URL of the given Blog: %s."
		response2="Avatar of the given Blog: %s."
		response3="Ask_title of the Blog: %s."
		response4="Description of the Blog is: %s." 
		return HttpResponse(response1 % url + "<br>" + response2 % avatar + "<br>" + response3 % ask_title + "<br>" + response4 % description)
	else:
		return HttpResponse("Please click the Button otherwise you will not get nothing")

def tum2(request):
	if request.method=='POST':
		word=request.POST['name']
		popular_word=tumblr2(word)
		response="Popular words in the posts of given tag are: %s."
		return HttpResponse(response % popular_word)
	else:
		return HttpResponse("Please click the Button otherwise you will not get nothing")

def tum3(request):
	if request.method=='POST':
		word=request.POST['name']
		nu=request.POST['num']
		blog=tumblr3(word,nu)
		response="Details of the blog is: %s."
		return HttpResponse(response % blog)
	else:
		return HttpResponse("Please click the Button otherwise you will not get nothing")

def tum4(request):
	if request.method=='POST':
		blog_name=request.POST['name']
		[popular_words,popular_tags]=tumblr4(blog_name)
		response1="Popular words in the posts of given blog are: %s."
		response2="Popular tags in the posts of given blog are: %s."
		return HttpResponse(response1 % popular_words + "<br>" + response2 % popular_tags)
	else:
		return HttpResponse("Please click the Button otherwise you will not get nothing")

def tum5(request):
	if request.method=='POST':
		word=request.POST['name']
		num=request.POST['num']
		tagg=tumblr5(word,num)
		response="Details of the blogs with this tags are: %s."
		return HttpResponse(response % tagg)
	else:
		return HttpResponse("Please click the Button otherwise you will not get nothing")


def yt1(request):
	if request.method=='POST':
		keyword=request.POST['name']
		return HttpResponse(youtube1(keyword))
	else:
		return HttpResponse("Please click the Button otherwise you will not get nothing")

def yt2(request):
	if request.method=='POST':
		keyword=request.POST['name']
		num=request.POST['handle']
		popular_word=youtube2(keyword,num)
		response="Videos of the given channel with given keyword: %s."
		return HttpResponse(response % popular_word)
	else:
		return HttpResponse("Please click the Button otherwise you will not get nothing")

def yt3(request):
	if request.method=='POST':
		keyword=request.POST['name']
		nu=request.POST['num']
		popular_word=youtube3(keyword,nu)
		response="Videos of the given keyword and given appearances: %s."
		return HttpResponse(response % popular_word)
	else:
		return HttpResponse("Please click the Button otherwise you will not get nothing")

def ins1(request):
	if request.method=='POST':
		access=request.POST['access']
		[biography,name,picture,web]=instagram1(access)
		response1="Biography of the user is: %s."
		response2="Name of the user is: %s."
		response3="Picture of the user is: %s."
		response4="website of the user is: %s."
		return HttpResponse(response1 % biography + "<br>" + response2 % name + "<br>" + response3 % picture + "<br>" + response4 % web)
	else:
		return HttpResponse("Please click the Button otherwise you will not get nothing")

def ins2(request):
	if request.method=='POST':
		access=request.POST['access']
		return HttpResponse(instagram2(access))
	else:
		return HttpResponse("Please click the Button otherwise you will not get nothing")

def red1(request):
	if request.method=='POST':
		name=request.POST['user']
		response="Graphs are shown and details about the input is given: %s."
		result=reddit1(name)
		return HttpResponse(response % result)
	else:
		return HttpResponse("Please click the Button otherwise you will not get nothing")

def red2(request):
	if request.method=='POST':
		user=request.POST['user']
		name=request.POST['name']
		response="Graphs are shown and details about the input author is given: %s."
		result=reddit2(user,name)
		return HttpResponse(response % result)
	else:
		return HttpResponse("Please click the Button otherwise you will not get nothing")

def red3(request):
	if request.method=='POST':
		user=request.POST['user']
		num=request.POST['num']
		response="Graphs are shown and details about the input number of posts is given: %s."
		result=reddit3(user,num)
		return HttpResponse(response % result)
	else:
		return HttpResponse("Please click the Button otherwise you will not get nothing")


