import logging

from django.contrib import admin

from core.models import Feed, FeedReview, FeedItem

log = logging.getLogger(__name__)  # Get an instance of a logger


class FeedAdmin(admin.ModelAdmin):
    list_display = ('date_created',)
admin.site.register(Feed, FeedAdmin)


class FeedReviewAdmin(admin.ModelAdmin):
    list_display = ('feed', 'user', 'score', 'title',)
admin.site.register(FeedReview, FeedReviewAdmin)


class FeedItemAdmin(admin.ModelAdmin):
    list_display = ('feed', 'author', 'title',)
admin.site.register(FeedItem, FeedItemAdmin)

