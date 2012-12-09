#coding=utf-8

from django import http
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext_lazy, ugettext as _
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext

from core.forms import CreateFeedForm
from core.models import Feed, FeedItem, FeedSubscriber


@login_required
def feed_create(request):
    """
    Creates a feed
    """
    user = get_object_or_404(User, id=request.user.id)
    my_feeds = Feed.objects.filter(publisher=user, )

    form = CreateFeedForm()

    if request.method == 'POST':
        form = CreateFeedForm(request.POST)

        if form.is_valid():
            feed = form.save(user=user)
            url = reverse('feed_detail_dashboard', args=[
                feed.publisher.username,
                feed.slug
            ])
            return HttpResponseRedirect(url)

    return render_to_response('core/feeds/create.html', {
        'form': form,
        'my_feeds': my_feeds,
        'page_name': 'feed_create',
    }, RequestContext(request))


@login_required
def feed_subscriptions(request):
    """
    User subscriptions view
    """
    user = get_object_or_404(User, username=request.user.username)
    my_feeds = Feed.objects.filter(publisher=user, )
    feeds = [x.feed for x in FeedSubscriber.objects.filter(user=user).select_related('feed')]
    channel_name = '{0} Channels'.format(user.get_full_name().title() + "'s")

    return render_to_response('core/feeds/subscriptions.html', {
        'profile': user.profile,
        'feeds': feeds,
        'my_feeds': my_feeds,
        'page_name': 'feed_subscriptions',
    }, RequestContext(request))


def feed_detail(request, username, feed_slug):
    """
    Users feed detail
    """
    user = get_object_or_404(User, username=username)
    feed = get_object_or_404(Feed, publisher=user, slug=feed_slug)
    filter_options = FeedItem.TYPE_CHOICES

    if not feed.is_subscribed(user):
        return HttpResponseRedirect(reverse('feed_detail_subscribe'), args={ 'username': username, 'feed_slug': feed_slug })

    return render_to_response('core/feeds/detail.html', {
        'profile': user.profile,
        'feed': feed,
        'filter_options': filter_options,
        'page': 'feeds',
    }, RequestContext(request))

def feed_detail_subscribe(request, username, feed_slug):
    """
    Users feed detail
    """
    user = get_object_or_404(User, username=username)
    feed = get_object_or_404(Feed, publisher=user, slug=feed_slug)
    feed_items = FeedItem.objects.filter(feed=feed, is_sample=True)[:3]

    return render_to_response('core/feeds/detail_subscribe.html', {
        'profile': user.profile,
        'feed': feed,
        'feed_items': feed_items,
        'page': 'feeds',
    }, RequestContext(request))

def feed_detail_dashboard(request, username, feed_slug):
    """
    Users feed dashboard
    """
    user = get_object_or_404(User, username=username)
    feed = get_object_or_404(Feed, publisher=user, slug=feed_slug)
    my_feeds = Feed.objects.filter(publisher=user, )
    feed_items = FeedItem.objects.filter(feed=feed, is_sample=True)[:3]

    return render_to_response('core/feeds/dashboard.html', {
        'profile': user.profile,
        'feed': feed,
        'my_feeds': my_feeds,
        'feed_items': feed_items,
        'page': 'feeds',
    }, RequestContext(request))

def feed_item_detail(request, username, feed_slug, item_slug):
    """
    Users feed item detail
    """
    user = get_object_or_404(User, username=username)
    feed_item = get_object_or_404(FeedItem, feed__publisher=user, feed__slug=feed_slug, slug=item_slug)

    return render_to_response('core/feeds/detail.html', {
        'profile': user.profile,
        'item': feed_item,
    }, RequestContext(request))


