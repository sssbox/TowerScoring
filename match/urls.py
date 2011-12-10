from django.conf.urls.defaults import patterns, include, url

from django.conf import settings


urlpatterns = patterns('match.views',
    url(r'^finished_scoring_center/$', 'finished_scoring_center', \
            name='match_finished_scoring_center'),
)
