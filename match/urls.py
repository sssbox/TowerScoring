from django.conf.urls.defaults import patterns, include, url

from django.conf import settings


urlpatterns = patterns('match.views',
    # Mobile Scorer
    url(r'^finished_scoring_center/$', 'finished_scoring_center', \
            name='match_finished_scoring_center'),
    url(r'^finished_scoring_match/$', 'finished_scoring_match', \
            name='match_finished_scoring_match'),
    url(r'^check_scorer_status/$', 'check_scorer_status', \
            name='match_check_scorer_status'),
    url(r'^score_event/$', 'score_event', name='match_score_event'),

    # Scorekeeper Controller
    url(r'^pick_scorer/$', 'pick_scorer', name='match_pick_scorer'),
    url(r'^select_match/$', 'select_match', name='match_select_match'),
    url(r'^delete_match_event/$', 'delete_match_event', name='match_delete_match_event'),
    url(r'^start_match/$', 'start_match', name='match_start_match'),
    url(r'^reset_match/$', 'reset_match', name='match_reset_match'),
    url(r'^robot_present/$', 'robot_present', name='match_robot_present'),
    url(r'^update_score/$', 'update_score', name='match_update_score'),
)
