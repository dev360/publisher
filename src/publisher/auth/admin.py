import logging

from django.contrib import admin

from auth.models import Profile

log = logging.getLogger(__name__)  # Get an instance of a logger

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('status', 'activation_key', 'user')

admin.site.register(Profile, ProfileAdmin)
