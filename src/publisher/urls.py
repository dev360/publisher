from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^jstools/', include('jstools.urls')),
    (r'^admin/', include(admin.site.urls)),

    (r'', include('auth.urls')),
    (r'', include('core.urls')), #namespace='core', app_name='core')),

    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
