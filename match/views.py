import datetime
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from models import *
try: import simplejson as json
except: import json

def get_microseconds():
    now = datetime.datetime.now()
    ms = now.microsecond
    ms += now.second * 1000000
    ms += now.minute * 60000000
    ms += now.hour * 3600000000
    return ms

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
                    match.save()
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
        elif 'center' in tower.name: # scoring on center tower
            if alliance == 'red':
                match.red_score += SCORE_SETTINGS[level]
                match.red_score_pre_penalty += SCORE_SETTINGS[level]
            else:
                match.blue_score += SCORE_SETTINGS[level]
                match.blue_score_pre_penalty += SCORE_SETTINGS[level]
        else: # alliance attempting to descore
            pass # TODO

# inputs POSTed:
# alliance = red or blue -- alliance who scored on the goal
# level = 1, 2 or 3 ( 1 low gv (or only gv), 2 high gv, 3 av score)
@staff_member_required
def score_event(request):
    scoring_device = ScoringDevice.objects.get(scorer=request.user)
    now = datetime.datetime.now()
    match = ScoringSystem.objects.all()[0].current_match
    if scoring_device.on_center:
        tower = Tower.objects.get(name='center')
    else:
        tower = scoring_device.tower
    alliance = request.POST.get('alliance', '')
    if not alliance:
        print 'Error!!! No alliance.' # TODO
    level = request.POST.get('level', '')
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
    tower_name = scoring_device.tower.name
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
    except:
        current_state, current_match = 'no_match', ''
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
