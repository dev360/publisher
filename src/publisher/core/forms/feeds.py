#coding=utf-8
from datetime import date
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _


from core.models import Feed
from utils import forms


class CreateFeedForm(forms.ModelForm):
    """ This form is for adding/editing the profile """

    def __init__(self, *args, **kwargs):
        super(CreateFeedForm, self).__init__(*args, **kwargs)

        placeholder_fields = ['title', 'description', 'image']
        for name in placeholder_fields:
            self.fields[name].widget.attrs = {
                'placeholder': self.fields[name].label,
                'class': 'input-large',
            }



    class Meta:
        model = Feed
