#coding=utf-8

from django import http
from django.db import transaction
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site, RequestSite
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext_lazy, ugettext as _
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext
from django.conf import settings

from auth.forms import AuthenticationForm, RegistrationForm
from core.models import Feed


def index(request):

    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('feed_subscriptions'))

    login_form = AuthenticationForm()
    registration_form = RegistrationForm()


    return render_to_response('core/index.html', {
        'feeds': Feed.objects.all(),
        'login_form': login_form,
        'registration_form': registration_form,
    }, RequestContext(request))



def channels(request):
    return render_to_response('core/channels.html', {
    }, RequestContext(request))

def terms_of_service(request):
    return render_to_response('core/misc/terms_of_service.html', {}, RequestContext(request))

def privacy_policy(request):
    return render_to_response('core/misc/privacy_policy.html', {}, RequestContext(request))


