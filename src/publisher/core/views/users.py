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


@login_required
def dashboard(request):
    """
    User detail view
    """
    user = get_object_or_404(User, username=request.user.username)
    feeds = user.feeds.all()
    channel_name = '{0} Channels'.format(user.get_full_name().title() + "'s")

    return render_to_response('core/users/dashboard.html', {
        'profile': user.profile,
        'feeds': feeds,
        'page': channel_name,
    }, RequestContext(request))


def user_detail(request, username):
    user = get_object_or_404(User, username=username)
    feeds = user.feeds.filter(publisher__username=username)
    channel_name = '{0} Channels'.format(user.get_full_name().title() + "'s")

    return render_to_response('core/users/detail.html', {
        'profile': user.profile,
        'feeds': feeds,
        'page': channel_name,
    }, RequestContext(request))


def user_share(request):
    """
    User detail view
    """
    user = get_object_or_404(User, id=request.user.id)

    form = CreateFeedForm()

    if request.method == 'POST':
        form = CreateFeedForm(request.POST)

        if form.is_valid():
            feed = form.save(user=user)
            url = reverse('feed_detail', args={
                'username': feed.publisher.username,
                'slug': feed.slug
            })
            return HttpResponseRedirect(url)

    return render_to_response('core/users/share.html', {
        'form': form,
        'page': 'share',
    }, RequestContext(request))

