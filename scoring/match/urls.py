from django.conf.urls.defaults import patterns, include, url

from django.conf import settings


urlpatterns = patterns('scoring.match.views',
    # Mobile Scorer
    url(r'^batch_actions/$', 'batch_actions', name='match_batch_actions'),

    # Scorekeeper Controller
    url(r'^pick_scorer/$', 'pick_scorer', name='match_pick_scorer'),
    url(r'^select_match/$', 'select_match', name='match_select_match'),
    url(r'^delete_match_event/$', 'delete_match_event', name='match_delete_match_event'),
    url(r'^start_match/$', 'start_match', name='match_start_match'),
    url(r'^reset_match/$', 'reset_match', name='match_reset_match'),
    url(r'^robot_present/$', 'robot_present', name='match_robot_present'),
    url(r'^update_score/$', 'update_score', name='match_update_score'),
)
