import datetime
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import Group
from models import *
from utils.time import get_microseconds
from scoring.views import scorekeeper
from match.tower_state import *

try: import simplejson as json
except: import json

#TODO create celery to automatically start the warning sequence at end of center tower activation
# or do pseudo cron on status requests from score/timer displays, etc.

# Allows us to easily implement ability to replay a match if we wanted to by iterating through Match Events
#       This would be probably necessary in order to implement "undo"
def update_from_match_event(me):
    alliance = me.alliance
    tower = me.tower
    match = me.match
    level = me.level
    # TODO Change lighting whenever '*.state' changes
    if '_' in tower.name: # low or high alliance tower
        if alliance in tower.name: # alliance scoring in own goal
            tl_1 = tower.towerlevel_set.get(level=1)
            if str(level) == str(1) or tl_1.state != alliance:
                tl = tl_1
            else:
                tl = tower.towerlevel_set.get(level=2)
            if tl.state != alliance and tl.state != 'off': # It is scorable
                tl.state = alliance
                tl.save()
                alliance_towers = TowerLevel.objects.filter(tower__name__contains='_'+alliance)
                alliance_towers_uncharged = alliance_towers.exclude(state=alliance)
                # Check for alliance fully charged, turn all to off if they are now charged
                if not alliance_towers_uncharged.exists() \
                        and ((alliance == 'blue' and not match.blue_center_active) \
                                or (alliance == 'red' and not match.red_center_active)):
#TODO if other timer is running and there is < 5 seconds left, set cur to other_time+5
                    if alliance == 'blue':
                        match.blue_center_active = True
                        match.blue_center_active_start = datetime.datetime.now()
                    else:
                        match.red_center_active = True
                        match.red_center_active_start = datetime.datetime.now()
                    alliance_towers.update(state='off')
                    center = Tower.objects.get(name='center')
                    low_center = center.towerlevel_set.get(level=1)
                    if (alliance == 'blue' and not match.red_center_active) \
                            or (alliance == 'red' and not match.blue_center_active):
                        low_center.state = alliance
                    else:
                        low_center.state = 'purple'
                    alliance_scorers = ScoringDevice.objects.filter(tower__name__contains='_'+alliance)
                    alliance_scorers.update(on_center=True)
                if alliance == 'red':
                    match.red_score += SCORE_SETTINGS[level]
                    match.red_score_pre_penalty += SCORE_SETTINGS[level]
                else:
                    match.blue_score += SCORE_SETTINGS[level]
                    match.blue_score_pre_penalty += SCORE_SETTINGS[level]
        else: # alliance attempting to descore
            pass # TODO
    elif 'center' in tower.name: # scoring on center tower
        if alliance == 'red':
            match.red_score += SCORE_SETTINGS[level]
            match.red_score_pre_penalty += SCORE_SETTINGS[level]
        else:
            match.blue_score += SCORE_SETTINGS[level]
            match.blue_score_pre_penalty += SCORE_SETTINGS[level]
    match.save()
    return match

# inputs POSTed:
# alliance = red or blue -- alliance who scored on the goal
# level = 1, 2 or 3 ( 1 low gv (or only gv), 2 high gv, 3 av score)
# TODO allow batched match events coming in in case there is a communication hickup
# TODO get uniqueIDs from each scoring device per match event so that match events
#      can't be duplicated... Also say which match events are properly saved
#      in each reponse so that events can come off the queue at the scoring device.
@staff_member_required
def score_event(request):
    scoring_device = ScoringDevice.objects.get(scorer=request.user)
    now = datetime.datetime.now()
    match = ScoringSystem.objects.all()[0].current_match
    if scoring_device.on_center:
        tower = Tower.objects.get(name='center')
    else:
        tower = scoring_device.tower
    alliance = request.GET.get('alliance', '')
    if not alliance:
        print 'Error!!! No alliance.' # TODO
    level = request.GET.get('level', '')
    if not level:
        print 'Error!!! No level.' # TODO
    me = MatchEvent(match=match, microseconds=get_microseconds(), \
            scorer=request.user, tower=tower, alliance=alliance, \
            level=int(level))
    me.save()

    update_from_match_event(me)
    return HttpResponse(json.dumps({'success': True}), 'application/json')

@staff_member_required
def finished_scoring_center(request):
    scoring_device = ScoringDevice.objects.get(scorer=request.user)
    if scoring_device.on_center:
        scoring_device.on_center = False
        scoring_device.save()
    return HttpResponse(json.dumps({'success': True}), 'application/json')

@staff_member_required
def finished_scoring_match(request):
    scoring_device = ScoringDevice.objects.get(scorer=request.user)
    tower_name = scoring_device.tower.name
    match = ScoringSystem.objects.all()[0].current_match
    if   tower_name == 'low_red':    match.scorer_low_red_confirmed = True
    elif tower_name == 'high_red':   match.scorer_high_red_confirmed = True
    elif tower_name == 'low_blue':   match.scorer_low_blue_confirmed = True
    elif tower_name == 'high_blue':  match.scorer_high_blue_confirmed = True
    match.save()
    return HttpResponse(json.dumps({'success': True}), 'application/json')

@staff_member_required
def check_scorer_status(request):
    scoring_device = ScoringDevice.objects.get(scorer=request.user)
    scoring_device.last_contact = datetime.datetime.now()
    scoring_device.save()
    try: tower_name = scoring_device.tower.name
    except:
        return HttpResponse(json.dumps({'current_state':'no_match','current_match':''}),'application/json')
    current_state, current_match = '', ''
    try:
        match = ScoringSystem.objects.all()[0].current_match
        current_match = str(match.id)
        if not match.actual_start:
            current_state = 'prematch'
        else:
            timer = (match.actual_start + datetime.timedelta(seconds=150)) - datetime.datetime.now()
            if timer.days < 0:
                if   tower_name == 'low_red':   confirmed = match.scorer_low_red_confirmed
                elif tower_name == 'high_red':  confirmed = match.scorer_high_red_confirmed
                elif tower_name == 'low_blue':  confirmed = match.scorer_low_blue_confirmed
                elif tower_name == 'high_blue': confirmed = match.scorer_high_blue_confirmed
                if confirmed:
                    current_state = 'match_done_confirmed'
                else:
                    current_state = 'match_done_not_confirmed'
    except: current_state, current_match = 'no_match', ''
    if not current_state:
        if '_red' in tower_name:
            center_start = match.red_center_active_start
        else:
            center_start = match.blue_center_active_start
        try:
            diff = (center_start + datetime.timedelta(seconds=30)) - datetime.datetime.now()
            if diff.days < 0: current_state = 'normal'
            else: current_state = 'center'
        except: current_state = 'normal'
    return HttpResponse(json.dumps({'current_state': current_state,  \
            'current_match':current_match}), 'application/json')


# Scorekeeper Functions
@staff_member_required
def pick_scorer(request):
    group = Group.objects.get(name='Scorekeepers')
    if group not in request.user.groups.all():
        raise Http404
    match = ScoringSystem.objects.all()[0].current_match
    tower_name = request.GET.get('tower_name', '')
    scorer_id = request.GET.get('scorer_id', '')

    if tower_name == 'low_red':
        try:
            sd = match.scorer_low_red.scoringdevice
            sd.tower = None
            sd.save()
        except: pass
        if str(scorer_id) == '0': match.scorer_low_red = None
        else: match.scorer_low_red_id = scorer_id
    elif tower_name == 'high_red':
        try:
            sd = match.scorer_high_red.scoringdevice
            sd.tower = None
            sd.save()
        except: pass
        if str(scorer_id) == '0': match.scorer_high_red = None
        else: match.scorer_high_red_id = scorer_id
    elif tower_name == 'low_blue':
        try:
            sd = match.scorer_low_blue.scoringdevice
            sd.tower = None
            sd.save()
        except: pass
        if str(scorer_id) == '0': match.scorer_low_blue = None
        else: match.scorer_low_blue_id = scorer_id
    elif tower_name == 'high_blue':
        try:
            sd = match.scorer_high_blue.scoringdevice
            sd.tower = None
            sd.save()
        except: pass
        if str(scorer_id) == '0': match.scorer_high_blue = None
        else: match.scorer_high_blue_id = scorer_id

    match.save()
    if str(scorer_id) != '0':
        sd, _ = ScoringDevice.objects.get_or_create(scorer_id=scorer_id)
        sd.tower = Tower.objects.get(name = tower_name)
        sd.save()
    return scorekeeper(request)

@staff_member_required
def reset_match(request):
    group = Group.objects.get(name='Scorekeepers')
    if group not in request.user.groups.all():
        raise Http404
    match = ScoringSystem.objects.all()[0].current_match
    match.reset()
    ScoringDevice.objects.all().update(on_center=False)

    #TODO change to end_match_lighting+add a delayed task for starting prematch lighting
    prematch_lighting()
    return scorekeeper(request)

@staff_member_required
def start_match(request):
    group = Group.objects.get(name='Scorekeepers')
    if group not in request.user.groups.all():
        raise Http404
    match = ScoringSystem.objects.all()[0].current_match
    match.reset()
    ScoringDevice.objects.all().update(on_center=False)
    match.actual_start = datetime.datetime.now()
    match.save()
    start_match_lighting()
    return scorekeeper(request)

@staff_member_required
def robot_present(request):
    group = Group.objects.get(name='Scorekeepers')
    if group not in request.user.groups.all():
        raise Http404
    match = ScoringSystem.objects.all()[0].current_match
    code = request.GET.get('code', '')
    state = request.GET.get('is_present', 'False') == 'True'
    if code == 'red_team_1_has_av': match.red_1_av_present = state
    elif code == 'red_team_2_has_av': match.red_2_av_present = state
    elif code == 'red_team_1_has_gv': match.red_1_gv_present = state
    elif code == 'red_team_2_has_gv': match.red_2_gv_present = state
    elif code == 'blue_team_1_has_av': match.blue_1_av_present = state
    elif code == 'blue_team_2_has_av': match.blue_2_av_present = state
    elif code == 'blue_team_1_has_gv': match.blue_1_gv_present = state
    elif code == 'blue_team_2_has_gv': match.blue_2_gv_present = state
    match.save()
    return HttpResponse(json.dumps({'success': True}), 'application/json')

@staff_member_required
def update_score(request):
    group = Group.objects.get(name='Scorekeepers')
    if group not in request.user.groups.all():
        raise Http404
    match = ScoringSystem.objects.all()[0].current_match
    match.blue_score_pre_penalty = int(request.GET.get('blue_score_pre_penalty', '0'))
    match.red_score_pre_penalty = int(request.GET.get('red_score_pre_penalty', '0'))
    match.blue_penalties = int(request.GET.get('blue_penalties', '0'))
    match.red_penalties = int(request.GET.get('red_penalties', '0'))
    match.blue_bonus = int(request.GET.get('blue_bonus', '0'))
    match.red_bonus = int(request.GET.get('red_bonus', '0'))
    match.calculate_scores()
    match.red_1.update_points()
    match.red_2.update_points()
    match.blue_1.update_points()
    match.blue_2.update_points()
    return HttpResponse(json.dumps({'success': True}), 'application/json')

@staff_member_required
def select_match(request):
    group = Group.objects.get(name='Scorekeepers')
    if group not in request.user.groups.all():
        raise Http404
    ss = ScoringSystem.objects.all()[0]
    match = Match.objects.get(id=request.GET.get('match_id'))
    ss.current_match = match
    ss.save()
    if not match.actual_start:
        for sd in ScoringDevice.objects.filter(tower__isnull=False):
            if sd.tower.name == 'low_red': match.scorer_low_red = sd.scorer
            elif sd.tower.name == 'high_red': match.scorer_high_red = sd.scorer
            elif sd.tower.name == 'low_blue': match.scorer_low_blue = sd.scorer
            elif sd.tower.name == 'high_blue': match.scorer_high_blue = sd.scorer
        match.save()
    prematch_lighting()
    return scorekeeper(request)

@staff_member_required
def delete_match_event(request):
    group = Group.objects.get(name='Scorekeepers')
    if group not in request.user.groups.all():
        raise Http404
    me = MatchEvent.objects.get(id=request.GET.get('me_id'))
    me.delete()

    match = ScoringSystem.objects.all()[0].current_match
    match.reset_score()
    start_match_lighting(dry_run_only=True)
    for me in match.matchevent_set.all().order_by('id'):
        match = update_from_match_event(me)
    match.calculate_scores()
    return scorekeeper(request)
