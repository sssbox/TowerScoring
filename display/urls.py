from django.conf.urls.defaults import patterns, include, url

from django.conf import settings


urlpatterns = patterns('display.views',
    url(r'^$', 'display', name='display_home'),
    url(r'^update_display/$', 'update_display', name='display_update'),
)
