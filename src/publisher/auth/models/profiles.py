#coding=utf-8
import hashlib
import random
import urllib
import datetime, os, linecache
from os.path import join as pjoin

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import permalink
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

try:
    from django.utils.timezone import now as datetime_now
except ImportError:
    datetime_now = datetime.datetime.now


from utils.models import GUIDModel


SITE_NAME = getattr(settings, 'SITE_NAME')
BASE_URL = getattr(settings, 'BASE_URL')


class ProfileManager(models.Manager):
    """ Manager for the profile object """

    def get_query_set(self):
        uber = super(ProfileManager, self)
        return uber.get_query_set().select_related('user')



PROFILE_STATUS_CHOICES = (
    ('NEW', _('New')),
    ('REG', _('Registered')),
)

class Profile(GUIDModel):
    """
    Profile object with some basic contact
    information.
    """
    status = models.CharField(_('status'), max_length=10, editable=True, default='NEW', choices=PROFILE_STATUS_CHOICES)
    activation_key = models.CharField(_('activation key'), editable=True, default='', max_length=100)
    user = models.OneToOneField(User, verbose_name=_('user'), related_name='profile', editable=True, unique=True)

    objects = ProfileManager()

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def gravatar_image(self):
        """
        Returns the gravatar image url
        """
        size = 32

        # construct the url
        base_url = "http://www.gravatar.com/avatar.php?{0}"
        params = {
            'gravatar_id': hashlib.md5(self.user.email.lower()).hexdigest(),
            'size':str(size)
        }
        return base_url.format(urllib.urlencode(params))

    def save(self, **kwargs):
        if not self.id:
            self.slug = self.user.username

        super(Profile, self).save(**kwargs)

    @permalink
    def get_absolute_url(self):
        return ('profile-view', None, {'slug': self.slug})

    def set_activation_key(self):

        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        username = self.user.username
        if isinstance(username, unicode):
            username = username.encode('utf-8')

        self.user.date_joined = datetime_now()
        self.activation_key = hashlib.sha1(salt+username).hexdigest()
        self.save()

    @property
    def activation_key_expired(self):
        """
        Determine whether this ``RegistrationProfile``'s activation
        key has expired, returning a boolean -- ``True`` if the key
        has expired.

        Key expiration is determined by a two-step process:

        1. If the user has already activated, the key will have been
           reset to the string constant ``ACTIVATED``. Re-activating
           is not permitted, and so this method returns ``True`` in
           this case.

        2. Otherwise, the date the user signed up is incremented by
           the number of days specified in the setting
           ``ACCOUNT_ACTIVATION_DAYS`` (which should be the number of
           days after signup during which a user is allowed to
           activate their account); if the result is less than or
           equal to the current date, the key has expired and this
           method returns ``True``.

        """
        expiration_date = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        return self.activation_key == self.ACTIVATED or \
               (self.user.date_joined + expiration_date <= datetime_now())

    def send_activation_email(self):
        """
        Sends an activation email to the user associated with this
        profile.
        """
        url = '{0}{1}'.format(BASE_URL, reverse('activate', args=[self.activation_key,]))

        ctx_dict = {'activation_url': url,
                    'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                    'SITE_NAME': SITE_NAME}
        subject = render_to_string('auth/activation_email_subject.txt',
                                   ctx_dict)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())

        message = render_to_string('auth/activation_email.txt',
                                   ctx_dict)

        self.user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

    def __unicode__(self):
        return self.user.username

    class Meta:
        app_label = 'core'
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')

