from django.conf.urls import patterns, url
import os

from GiftManage import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^gethistory/$', views.gethistory, name='gethistory'),
    url(r'^home/$', views.home, name='home'),
    url(r'^getfriendrequest/$', views.getfriendrequest, name='getfriendrequest'),
    url(r'^getfriends/$', views.getfriends, name='getfriends'),
    url(r'^getgifts/$', views.getgifts, name='getgifts'),
    url(r'^getgiftdetail/$', views.getgiftdetail, name='getgiftdetail'),
    url(r'^getfunds/$', views.getfunds, name='getfunds'),
    url(r'^searchfriend/$', views.searchfriend, name='searchfriend'),
    url(r'^addfriend/$', views.addfriend, name='addfriend'),
    url(r'^acceptfriend/$', views.acceptfriend, name='acceptfriend'),
    url(r'^publishgift/$', views.publishgift, name='publishgift'),
    url(r'^publishfund/$', views.publishfund, name='publishfund'),
    # url(r'^saveRelation/$', views.saveRelation, name='saveRelation'),
    url(r'^image/(?P<path>.*)','django.views.static.serve',{'document_root':os.path.join(os.path.dirname(__file__)) + '/resource/image/'}),
    url(r'^js/(?P<path>.*)','django.views.static.serve',{'document_root':os.path.join(os.path.dirname(__file__)) + '/resource/js/'}),
    url(r'^css/(?P<path>.*)','django.views.static.serve',{'document_root':os.path.join(os.path.dirname(__file__)) + '/resource/css/'}),  
    url(r'^files/(?P<path>.*)','django.views.static.serve',{'document_root':os.path.join(os.path.dirname(__file__)) + '/resource/files/'}),
)