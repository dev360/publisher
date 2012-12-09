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
from core.models import Feed

def feed_detail(request, username, slug):
    """
    User detail view
    """
    user = get_object_or_404(User, username=username)
    feed = Feed.objects.get(publisher=user, slug=slug)

    return render_to_response('core/feeds/detail.html', {
        'profile': user.profile,
        'feed': feed,
        'page': 'feeds',
    }, RequestContext(request))


