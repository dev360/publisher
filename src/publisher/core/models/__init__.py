from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _


class Tag(models.Model):
    """
    Feed
    """

    name = models.CharField(_('name'), max_length=50, unique=True)

    class Meta:
        app_label = 'core'

    def __unicode__(self):
        return u'%s' % self.name


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

    publisher = models.ForeignKey(User, verbose_name=_('publisher'), related_name="feeds")
    subscribers = models.ManyToManyField(User, through='FeedSubscriber')
    title = models.CharField(_('channel name'), max_length=70) # NEVER CHANGE: for twitter
    slug = models.CharField(_('slug'), max_length=200, editable=False)
    description = models.TextField(_('channel description'))
    image = models.URLField(_('channel image'), null=True, blank=True)
    price_plan = models.IntegerField(_('price plan'), choices=PRICE_CHOICES, default=1)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)

    def __unicode__(self):
        return u'%s' % self.title

    def is_subscribed(self, user):
        return user.subscriptions.filter(feed=self).exists()

    def posts_per_month(self):
        query = """
            select count(*)
            from core_feed
            where
            date_created >= (CURRENT_DATE - INTERVAL '1 months')
        """
        results = self.feed_items.extra(select={'monthly_count': query})
        return results[0].monthly_count if len(results) > 0 else 0

    def subscribers_count(self):
        return self.subscribers.count()

    def reviews_count(self):
        return self.reviews.count()

    def likes_count(self):
        return Like.objects.filter(feed_item__in=self.feed_items.all()).count()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Feed, self).save(*args, **kwargs)

    class Meta:
        app_label = 'core'
        unique_together = ('publisher', 'slug',)

class FeedSubscriber(models.Model):
    """
    Feed Subscriber
    """

    feed = models.ForeignKey(Feed, verbose_name=_('feed'), db_index=True)
    user = models.ForeignKey(User, verbose_name=_('user'), related_name='subscriptions', db_index=True)
    start_date = models.DateTimeField(_('start date'), auto_now_add=True)

    class Meta:
        app_label = 'core'
        unique_together = ('feed', 'user',)


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

    class Meta:
        app_label = 'core'

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

    feed = models.ForeignKey(Feed, related_name="feed_items")
    title = models.CharField(_('title'), max_length=70) # NEVER CHANGE: for twitter
    slug = models.CharField(_('slug'), max_length=200, editable=False)
    teaser = models.TextField(_('teaser'), blank=True)
    text = models.TextField(_('text'), blank=True)
    is_sample = models.BooleanField(_('is sample'), default=False)
    type = models.CharField(_('type'), max_length=50, choices=TYPE_CHOICES, default='other', blank=True)
    file = models.FileField(_('file'), upload_to='attachments', blank=True)
    tags = models.ManyToManyField(Tag)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)

    class Meta:
        app_label = 'core'
        unique_together = ('feed', 'slug',)

    def __unicode__(self):
        return u'%s' % self.title

    def save(self, **kwargs):
        self.slug = slugify(self.title)
        super(FeedItem, self).save(**kwargs)


class Like(models.Model):
    user = models.ForeignKey(User, related_name="likes")
    feed_item = models.ForeignKey(FeedItem, related_name="likes")

    class Meta:
        app_label = 'core'
