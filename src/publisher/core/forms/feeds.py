#coding=utf-8
from datetime import date
from django.conf import settings
from django.forms import widgets
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _


from core.models import Feed
from utils import forms


class CreateFeedForm(forms.Form):
    """
    This form is for adding/editing the profile
    """
    title = forms.CharField(label=_('Feed name'), max_length=70)
    description = forms.CharField(label=_('Feed description'))
    image = forms.URLField(label=_('Feed image'), required=False)
    price_plan = forms.ChoiceField(label=_('Price'), widget=widgets.RadioSelect)

    def __init__(self, *args, **kwargs):
        super(CreateFeedForm, self).__init__(*args, **kwargs)

        self.fields['price_plan'].choices = Feed.PRICE_CHOICES

        placeholder_fields = ['title', 'description', 'image']
        for name in placeholder_fields:
            self.fields[name].widget.attrs = {
                'placeholder': self.fields[name].label,
                'class': 'input-large',
            }

    def save(self, *args, **kwargs):
        feed = None

        if self.is_valid():

            data = dict(
                title = self.cleaned_data['title'],
                description = self.cleaned_data['description'],
                image = self.cleaned_data['image'],
                price_plan = self.cleaned_data['price_plan'],
                publisher = kwargs.get('user'),
            )

            feed = Feed(**data)
            feed.save()

        return feed

