#coding=utf-8
from django.conf.urls.defaults import *
from django.utils.http import urlquote


from core import views

urlpatterns = patterns('',
    # Common views
    url(r'^$', views.index, name='index'),
    url(r'^channels/$', views.channels, name='channels'),

    # Misc views
    url(r'^terms/$', views.terms_of_service, name='terms-of-service'),
    url(r'^privacy/$', views.privacy_policy, name='privacy-policy'),

    # User views
    url(r'^create/$', views.feed_create, name='feed_create'),

    url(r'^subscriptions/$', views.feed_subscriptions, name='feed_subscriptions'),
    url(r'^channels/$', views.channels, name='channels'),

    url(r'^(?P<username>([^/])+)/$', views.user_detail, name='user_detail'),
    url(r'^(?P<username>([^/])+)/(?P<feed_slug>([^/])+)/$', views.feed_detail, name='feed_detail'),
    url(r'^(?P<username>([^/])+)/(?P<feed_slug>([^/])+)/create/$', views.feed_item_create, name='feed_item_create'),
    url(r'^(?P<username>([^/])+)/(?P<feed_slug>([^/])+)/subscribe/$', views.FeedDetailSubscribe.as_view(), name='feed_detail_subscribe'),
    url(r'^(?P<username>([^/])+)/(?P<feed_slug>([^/])+)/dashboard/$', views.feed_detail_dashboard, name='feed_detail_dashboard'),
    url(r'^(?P<username>([^/])+)/(?P<feed_slug>([^/])+)/(?P<item_slug>([^/])+)/$', views.feed_item_detail, name='feeditem_detail'),

)

