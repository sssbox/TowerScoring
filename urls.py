from django.conf.urls.defaults import patterns, include, url

from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'views.home', name='home'),
    # url(r'^scoring/', include('foo.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
       (r'^site_media/version[^/]+/(?P<path>.*)$', 'django.views.static.serve', \
            {'document_root': settings.MEDIA_ROOT}),
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', \
            {'document_root': settings.MEDIA_ROOT}),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', \
                {'document_root': settings.ADMIN_MEDIA_ROOT}),
    )
