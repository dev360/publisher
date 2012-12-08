#coding=utf-8

from django import http
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.cache import never_cache, cache_page
from django.utils.translation import ugettext_lazy, ugettext as _
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext

from app_auth.models import Profile
