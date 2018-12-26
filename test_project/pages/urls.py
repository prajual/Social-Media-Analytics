from django.urls import path

from . import  views
from .views import AboutPageView
from .views import FacebookGenerator
from .views import InstagramGenerator

urlpatterns = [
	path('facebook_access_token_generator/',FacebookGenerator.as_view(),name='facebook'),
	path('instagram_access_token_generator/',InstagramGenerator.as_view(),name='instagram'),
	path('fac/',views.user,name='user'),
	path('ins/',views.user1,name='user1'),
	path('facebook1/',views.fac1,name='fac1'),
	path('facebook2/',views.fac2,name='fac2'),
	path('facebook3/',views.fac3,name='fac3'),
	path('facebook4/',views.fac4,name='fac4'),
	path('twitter1/',views.tw1,name='tw1'),
	path('twitter2/',views.tw2,name='tw2'),
	path('twitter3/',views.tw3,name='tw3'),
	path('tumblr1/',views.tum1,name='tum1'),
	path('tumblr2/',views.tum2,name='tum2'),
	path('tumblr3/',views.tum3,name='tum3'),
	path('tumblr4/',views.tum4,name='tum4'),
	path('tumblr5/',views.tum5,name='tum5'),
	path('youtube1/',views.yt1,name='yt1'),
	path('youtube2/',views.yt2,name='yt2'),
	path('youtube3/',views.yt3,name='yt3'),
	path('instagram1/',views.ins1,name='ins1'),
	path('instagram2/',views.ins2,name='ins2'),
	path('reddit1/',views.red1,name='red1'),
	path('reddit2/',views.red2,name='red2'),
	path('reddit3/',views.red3,name='red3'),
	path('',AboutPageView.as_view(),name='about'),
]
