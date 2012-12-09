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
from django.views.generic import View
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext
from django.contrib.auth import authenticate

from auth.forms import RegistrationForm
from core.forms import CreateFeedForm, PaymentForm
from core.models import Feed, FeedItem

def feed_detail(request, username, feed_slug):
    """
    Users feed detail
    """
    user = get_object_or_404(User, username=username)
    feed = get_object_or_404(Feed, publisher=user, slug=feed_slug)

    if not feed.is_subscribed(user):
        return HttpResponseRedirect(reverse('feed_detail_subscribe'), args={ 'username': username, 'feed_slug': feed_slug })

    return render_to_response('core/feeds/detail.html', {
        'profile': user.profile,
        'feed': feed,
        'page': 'feeds',
    }, RequestContext(request))

class FeedDetailSubscribe(View):
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed

        self.request = request
        self.args = args
        self.kwargs = kwargs

        user = get_object_or_404(User, username=kwargs.get('username'))
        feed = get_object_or_404(Feed, publisher=user, slug=kwargs.get('feed_slug'))

        return handler(request, user, feed)

    def get(self, request, user, feed):
        return self.render(user, feed)

    def post(self, request, user, feed):
        register_form = None
        if self.request.user.is_anonymous():
            register_form = RegistrationForm(request.POST)
        subscribe_form = PaymentForm(request.POST)

        if ((register_form and register_form.is_valid()) or register_form == None) and subscribe_form.is_valid():
            if register_form:
                register_user = register_form.save(request)
                register_user.profile.status = 'REG'
                register_user.profile.save()

                registed_user = authenticate(
                    username=request.POST.get('username'),
                    password=request.POST.get('password')
                )

            register_form.save(request)

        return self.render(user, feed, register_form, subscribe_form)

    def render(self, user, feed, register_form=None, subscribe_form=PaymentForm()):
        if not register_form and self.request.user.is_anonymous():
            register_form = RegistrationForm()

        feed_items = FeedItem.objects.filter(feed=feed, is_sample=True)[:3]

        return render_to_response('core/feeds/detail_subscribe.html', {
            'profile': user.profile,
            'feed': feed,
            'feed_items': feed_items,
            'page': 'feeds',
            'register_form': register_form,
            'subscribe_form': subscribe_form
        }, RequestContext(self.request))


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


