#coding=utf-8
from django.conf.urls.defaults import *
from django.utils.http import urlquote


from core import views

urlpatterns = patterns('',
	# Common views
	url(r'^$', views.index, name='index'),

    # Misc views
    url(r'^terms/$', views.terms_of_service, name='terms-of-service'),
    url(r'^privacy/$', views.privacy_policy, name='privacy-policy'),

    # User views
	url(r'^(?P<username>([^/])+)/$', views.user_detail, name='user_detail'),
)

