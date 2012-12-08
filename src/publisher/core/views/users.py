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


def user_detail(request, username):
    """
    User detail view
    """
    user = get_object_or_404(User, username=username)
    feeds = [1, 2, 3]
    return render_to_response('core/users/detail.html', {
        'profile': user.profile,
        'feeds': feeds,
        'page': 'feeds',
    }, RequestContext(request))


def user_share(request):
    """
    User detail view
    """
    return render_to_response('core/users/share.html', {
        'page': 'share',
    }, RequestContext(request))

