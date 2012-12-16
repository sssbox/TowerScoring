from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'scoring.views.index', name='index'),
    url(r'^scorekeeper/$', 'scoring.views.scorekeeper', name='scorekeeper'),
    url(r'^test_ajax$', 'scoring.views.test_ajax', name='test_ajax'),
    url(r'^logout/$', 'scoring.views.logout', name='logout'),
    # url(r'^scoring/', include('foo.urls')),
    url(r'^match/', include('scoring.match.urls')),
    url(r'^display/', include('scoring.display.urls')),
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/favicon.ico'}),

    # Examples:
    # url(r'^$', 'scoring.views.home', name='home'),
    # url(r'^scoring/', include('scoring.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
#        (r'^static/(?P<path>.*)$', 'django.views.static.serve', \
#            {'document_root': settings.STATIC_ROOT}),
#        (r'^media/(?P<path>.*)$', 'django.views.static.serve', \
#                {'document_root': settings.ADMIN_MEDIA_ROOT}),
    )

