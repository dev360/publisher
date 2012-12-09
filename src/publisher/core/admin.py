import logging

from django.contrib import admin

from core.models import Feed, FeedReview, FeedItem, FeedSubscriber, Tag

log = logging.getLogger(__name__)  # Get an instance of a logger

class FeedSubscriberInline(admin.TabularInline):
    model = FeedSubscriber
    raw_id_fields = ('user',)
    extra = 1

class FeedAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'date_created',)
    raw_id_fields = ('publisher',)
    inlines = (FeedSubscriberInline,)
admin.site.register(Feed, FeedAdmin)


class FeedReviewAdmin(admin.ModelAdmin):
    list_display = ('feed', 'user', 'score', 'title',)
    raw_id_fields = ('feed', 'user',)
admin.site.register(FeedReview, FeedReviewAdmin)


class FeedItemAdmin(admin.ModelAdmin):
    list_display = ('feed', 'title',)
    raw_id_fields = ('feed',)
admin.site.register(FeedItem, FeedItemAdmin)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Tag, TagAdmin)

