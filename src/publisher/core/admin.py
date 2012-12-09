import logging

from django.contrib import admin

from core.models import Feed, FeedReview, FeedItem, FeedSubscriber

log = logging.getLogger(__name__)  # Get an instance of a logger

class FeedSubscriberInline(admin.TabularInline):
    model = FeedSubscriber
    extra = 1

class FeedAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'date_created',)
    inlines = (FeedSubscriberInline,)
admin.site.register(Feed, FeedAdmin)


class FeedReviewAdmin(admin.ModelAdmin):
    list_display = ('feed', 'user', 'score', 'title',)
admin.site.register(FeedReview, FeedReviewAdmin)


class FeedItemAdmin(admin.ModelAdmin):
    list_display = ('feed', 'title',)
admin.site.register(FeedItem, FeedItemAdmin)

