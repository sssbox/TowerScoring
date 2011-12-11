from django.conf.urls.defaults import patterns, include, url

from django.conf import settings


urlpatterns = patterns('match.views',
    url(r'^finished_scoring_center/$', 'finished_scoring_center', \
            name='match_finished_scoring_center'),
    url(r'^score_event/$', 'score_event', name='match_score_event'),
)
