from django.conf.urls.defaults import patterns, include, url

from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'views.index', name='index'),
    url(r'^scorekeeper/$', 'views.scorekeeper', name='scorekeeper'),
    url(r'^test_ajax$', 'views.test_ajax', name='test_ajax'),
    url(r'^logout/$', 'views.logout', name='logout'),
    # url(r'^scoring/', include('foo.urls')),
    url(r'^match/', include('match.urls')),
    url(r'^display/', include('display.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/site_media/favicon.ico'}),
)

if settings.DEBUG:
    urlpatterns += patterns('',
       (r'^site_media/version[^/]+/(?P<path>.*)$', 'django.views.static.serve', \
            {'document_root': settings.STATIC_ROOT}),
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', \
            {'document_root': settings.STATIC_ROOT}),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', \
                {'document_root': settings.ADMIN_MEDIA_ROOT}),
    )
