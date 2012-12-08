from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.db import models


class Feed(models.Model):
    """
    Feed
    """

    publishers = models.ManyToManyField(User, related_name="publishers+")
    subscribers = models.ManyToManyField(User, related_name="subscribers+", blank=True)
    title = models.CharField(_('title'), max_length=200)
    description = models.TextField(_('description'))
    image = models.URLField(_('image'), null=True, blank=True)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)

    def __unicode__(self):
        return self.title

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


class FeedItem(models.Model):
    """
    Feed Item
    """
    FEED_ITEMS_CHOICES = (
        ('audio', 'Audio'),
        ('picture', 'Picture'),
        ('text', 'Text'),
        ('video', 'Video'),
        ('other', 'Other'),
    )

    author = models.ForeignKey(User, related_name="authored")
    feed = models.ForeignKey(Feed, related_name="feed_items")
    title = models.CharField(_('title'), max_length=200)
    teaser = models.TextField(_('teaser'), blank=True)
    text = models.TextField(_('text'))
    is_sample = models.BooleanField(_('is sample'), default=False)
    type = models.CharField(_('type'), max_length=50, choices=FEED_ITEMS_CHOICES, default='other', blank=True)
    file = models.FileField(_('file'), upload_to='attachments', blank=True)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)


class Like(models.Model):
    user = models.ForeignKey(User, related_name="likes")
    feed_item = models.ForeignKey(FeedItem, related_name="likes")


