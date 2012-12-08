#coding=utf-8

from django import http
from django.contrib import auth
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

from auth.models import Profile
from auth.forms import ProfileForm, UserInvitationForm



@login_required
def profile_index(request):

    username = request.user.username
    url = reverse('user_detail', kwargs={ 'username': username })
    return HttpResponseRedirect(url)

@login_required
def profile_view(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    return render_to_response('auth/profiles/view.html', {'profile': profile}, RequestContext(request))


@login_required
def profile_add(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    return render_to_response('auth/profiles/add.html', {'profile': profile, 'form': form}, RequestContext(request))



@login_required
def profile_edit(request):
    profile = get_object_or_404(Profile, user__id=request.user.id)

    form = ProfileForm(instance=profile, initial={  })

    saved = False
    validation_error = False

    if request.method == 'POST':
        data = request.POST
        files = request.FILES
        form = ProfileForm(data, files, instance=profile)

        if form.is_valid():
            # Save profile.
            profile = form.save(user=request.user)
            profile.image = request.FILES.get('image')
            profile.status = 'REG'
            profile.save()
            saved = True

            form = ProfileForm(instance=profile, initial={  })

        else:
            validation_error = True

    args = {}
    args['profile'] = profile
    args['form'] = form

    args['saved'] = saved
    args['validation_error'] = validation_error
    return render_to_response('auth/profiles/edit.html', args, RequestContext(request))


@login_required
def profile_contact_edit(request):
    profile = get_object_or_404(Profile, user__id=request.user.id)

    form = ProfileForm(instance=profile, initial={ 'same_address': same_address })

    saved = False
    validation_error = False

    if request.method == 'POST':
        data = request.POST

        form = ProfileForm(data, instance=profile)

        if form.is_valid():

            form.save()
            saved = True

    args = {}
    args['profile'] = profile
    args['form'] = form

    args['saved'] = saved
    args['validation_error'] = validation_error
    return render_to_response('auth/profiles/edit_contact.html', args, RequestContext(request))


