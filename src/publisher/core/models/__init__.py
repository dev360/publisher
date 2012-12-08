from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.db import models


class Feed(models.Model):
    """
    Feed
    """

    publishers = models.ManyToManyField(User, related_name="publishers+")
    subscribers = models.ManyToManyField(User, related_name="subscribers+")
    title = models.CharField(_('title'), max_length=50)
    description = models.TextField(_('description'))
    image = models.URLField(_('image'), null=True)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)


class FeedReview(models.Model):
    """
    Feed Review
    """

    user = models.ForeignKey(User, related_name="reviews")
    score = models.IntegerField(_('score'), default=5)
    title = models.CharField(_('title'), max_length=50)
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

    feed = models.ForeignKey(Feed, related_name="feed_items")
    title = models.CharField(_('title'), max_length=50)
    teaser = models.TextField(_('teaser'))
    description = models.TextField(_('description'))
    is_sample = models.BooleanField(_('is sample'), default=False)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)
    type = models.CharField(_('type'), max_length=50, choices=FEED_ITEMS_CHOICES, default='other')
    file = models.FileField(_('file'), upload_to='attachments')


class Like(models.Model):
    user = models.ForeignKey(User, related_name="likes")
    feed_item = models.ForeignKey(FeedItem, related_name="likes")


