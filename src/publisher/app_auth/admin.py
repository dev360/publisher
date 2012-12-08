import logging

from django.contrib import admin

from app_auth.models import Profile

log = logging.getLogger(__name__)  # Get an instance of a logger

class ProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(Profile, ProfileAdmin)
