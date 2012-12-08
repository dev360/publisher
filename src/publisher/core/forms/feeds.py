#coding=utf-8
from datetime import date
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _


from core.models import Feed
from utils import forms


class CreateFeedForm(forms.ModelForm):
    """ This form is for adding/editing the profile """

    class Meta:
        model = Feed
