from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _


class Feed(models.Model):
    """
    Feed
    """

    PRICE_CHOICES = (
        (1, _('$1')),
        (2, _('$2')),
        (3, _('$3')),
        (4, _('$4')),
        (5, _('$5')),
    )

    publishers = models.ManyToManyField(User, related_name="publishers+")
    subscribers = models.ManyToManyField(User, related_name="subscribers+", blank=True)
    title = models.CharField(_('title'), max_length=70) # NEVER CHANGE: for twitter
    slug = models.CharField(_('slug'), max_length=200)
    description = models.TextField(_('description'))
    image = models.URLField(_('image'), null=True, blank=True)
    price_plan = models.IntegerField(_('price plan'), choices=PRICE_CHOICES, default=1)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)

    def __unicode__(self):
        return u'%s' % self.title

    def save(self, **kwargs):
        self.slug = slugify(self.title)
        super(Feed, self).save(**kwargs)

class FeedReview(models.Model):
    """
    Feed Review
    """

    feed = models.ForeignKey(Feed, related_name="reviews")
    user = models.ForeignKey(User, related_name="reviews")
    score = models.IntegerField(_('score'), default=5)
    title = models.CharField(_('title'), max_length=50, blank=True)
    description = models.TextField(_('description'))
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)

    def __unicode__(self):
        return u'User ID %s review of Feed ID %s, with a score of %s' % (self.user.id, self.feed.id, self.score)


class FeedItem(models.Model):
    """
    Feed Item
    """

    TYPE_CHOICES = (
        ('audio', _('Audio')),
        ('picture', _('Picture')),
        ('text', _('Text')),
        ('video', _('Video')),
        ('other', _('Other')),
    )

    author = models.ForeignKey(User, related_name="authored")
    feed = models.ForeignKey(Feed, related_name="feed_items")
    title = models.CharField(_('title'), max_length=70) # NEVER CHANGE: for twitter
    slug = models.CharField(_('slug'), max_length=200)
    teaser = models.TextField(_('teaser'), blank=True)
    text = models.TextField(_('text'), blank=True)
    is_sample = models.BooleanField(_('is sample'), default=False)
    type = models.CharField(_('type'), max_length=50, choices=TYPE_CHOICES, default='other', blank=True)
    file = models.FileField(_('file'), upload_to='attachments', blank=True)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)

    class Meta:
        unique_together = ('feed', 'slug',)

    def __unicode__(self):
        return u'%s' % self.title

    def save(self, **kwargs):
        self.slug = slugify(self.title)
        super(FeedItem, self).save(**kwargs)


class Like(models.Model):
    user = models.ForeignKey(User, related_name="likes")
    feed_item = models.ForeignKey(FeedItem, related_name="likes")


