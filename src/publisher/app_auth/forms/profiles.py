#coding=utf-8
from datetime import date
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _


from app_auth.models import User, Profile
from utils import forms


class ProfileForm(forms.ModelForm):
    """ This form is for adding/editing the profile """


    def __init__(self, *args, **kwargs):

        self.user = kwargs.pop('user', None)

        super(ProfileForm, self).__init__(*args, **kwargs)

        # Want to use placeholder for these fields ...
        #self.fields['first_name'].widget.attrs = { 'placeholder': self.fields['first_name'].label }
        #self.fields['last_name'].widget.attrs = { 'placeholder': self.fields['last_name'].label }

    def save(self, user=None):
        if not user:
            raise Exception("User has to be specified")

        if not self.is_valid():
            raise Exception("Form has to be valid before saving")

        profile = Profile.objects.get(user=user)

        data = self.cleaned_data

        profile.save()

        return profile

    class Meta:
        model = Profile


