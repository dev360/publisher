#coding=utf-8
from datetime import date
from django.conf import settings
from django.forms import widgets
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from core.models import Feed, FeedItem, FeedSubscriber
from core.fields import CreditCardField, ExpiryDateField, VerificationValueField
from utils import forms


class PaymentForm(forms.Form):
    """
    Credit Card form
    """
    name_on_card = forms.CharField(label=_('Name on card'), max_length=50, required=True)
    card_number = CreditCardField(label=_('Card number'), required=True)
    expiry_date = ExpiryDateField(required=True)
    card_code = VerificationValueField(label=_('CCV'), required=True)

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)


        for name in self.fields.keys():
            self.fields[name].widget.attrs = {
                'placeholder': self.fields[name].label,
                'class': 'input-large',
            }

class CreateFeedForm(forms.Form):
    """
    This form is for adding/editing the profile
    """
    title = forms.CharField(label=_('Channel name'), max_length=70)
    description = forms.CharField(label=_('Channel description'))
    image = forms.URLField(label=_('Channel image'), required=False)
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


class CreateFeedItemForm(forms.ModelForm):
    """
    This form is for adding feed items
    """
    def __init__(self, *args, **kwargs):
        super(CreateFeedItemForm, self).__init__(*args, **kwargs)

        for name in self.fields.keys():
            self.fields[name].widget.attrs = {
                'placeholder': self.fields[name].label,
                'class': 'input-large input-block-level',
            }


    class Meta:
        model = FeedItem

