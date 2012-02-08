import datetime, time
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import Group
from django.conf import settings
from celery.task.control import revoke

from models import *
from utils.time import get_microseconds
from scoring.views import scorekeeper, get_scorer_data # This is not a relative import
from match.tower_state import *
from utils.test_leds import update_test_led
from utils.field_leds import update_real_leds
from match.tasks import run_match, abort_match
from utils.sound import play_sound

try: import simplejson as json
except: import json

def update_from_match_event(me):
    alliance = me.alliance
    tower = me.tower
    match = me.match
    level = me.level
    if '_' in tower.name: # low or high alliance tower
        if alliance in tower.name: # alliance scoring in own goal
            tl_1 = tower.towerlevel_set.get(level=1)
            if str(level) == str(1) or tl_1.state != alliance or 'low_' in tower.name:
                tl = tl_1
            else:
                tl = tower.towerlevel_set.get(level=2)
            if tl.state == alliance or tl.state == 'off':
                me.dud = True
                me.save()
            else: # It is scorable
                if me.dud == True:
                    me.dud = False
                    me.save()
                tl.state = alliance
                tl.save()
                alliance_towers = TowerLevel.objects.filter(tower__name__contains='_'+alliance)
                alliance_towers_uncharged = alliance_towers.exclude(state=alliance)
                if not alliance_towers_uncharged.exists() \
                        and not getattr(match, alliance+'_center_active'):
                    center = Tower.objects.get(name='center')
                    low_center = center.towerlevel_set.get(level=1)
                    off_color = 'blue' if alliance=='red' else 'red'
                    setattr(match, alliance + '_center_active', True)
                    this_start = datetime.datetime.now()
                    if match.actual_start+datetime.timedelta(seconds=120) < this_start:
                        this_start = match.actual_start + datetime.timedelta(seconds=120)
                        if not getattr(match, off_color + '_center_active'):
                            low_center.state = alliance
                        else: low_center.state = 'purple'
                    elif not getattr(match, off_color + '_center_active'):
                        low_center.state = alliance
                    else:
                        low_center.state = 'purple'
                        other_start = getattr(match, off_color + '_center_active_start')
                        if (this_start - other_start).total_seconds() < 5.0:
                            td = datetime.timedelta(seconds=5)
                            this_start = other_start+td
                    setattr(match, alliance + '_center_active_start', this_start)
                    update_test_led(low_center)
                    update_real_leds(low_center)

                    alliance_towers.update(state='off')
                    for tl_alliance in alliance_towers:
                        update_test_led(tl_alliance)
                        update_real_leds(tl_alliance)
                    alliance_scorers = ScoringDevice.objects.filter(tower__name__contains='_'+alliance)
                    alliance_scorers.update(on_center=True)
                else:
                    update_test_led(tl)
                    update_real_leds(tl)
                if alliance == 'red':
                    match.red_score += SCORE_SETTINGS[level]
                    match.red_score_pre_penalty += SCORE_SETTINGS[level]
                else:
                    match.blue_score += SCORE_SETTINGS[level]
                    match.blue_score_pre_penalty += SCORE_SETTINGS[level]
        else: # alliance attempting to descore
            descoring_alliance = alliance
            if descoring_alliance == 'red': descored_alliance = 'blue'
            else: descored_alliance = 'red'

            try:
                tl_2 = tower.towerlevel_set.get(level=2)
            except:
                tl = tower.towerlevel_set.get(level=1)
                tl_2 = False
            else:
                if int(level) == 1 or tl_2.state != descored_alliance or 'low_' in tower.name:
                    tl = tower.towerlevel_set.get(level=1)
                else:
                    tl = tl_2

            if tl.state == descored_alliance and not \
                    (tl.level == 1 and tl_2 and tl_2.state == descored_alliance):
                tl.state = 'green'
                tl.save()
                update_test_led(tl)
                update_real_leds(tl)
                if me.dud == True:
                    me.dud = False
                    me.save()
            else:
                me.dud = True
                me.save()


    elif 'center' in tower.name: # scoring on center tower
        s = SCORE_SETTINGS[level]
        if me.undo_score: s = 0 - s
        if alliance == 'red':
            match.red_score += s
            match.red_score_pre_penalty += s
        else:
            match.blue_score += s
            match.blue_score_pre_penalty += s
    match.save()

def score_match_event(user, match, tower, key, data):
    if not MatchEvent.objects.filter(scorer=user, collision_id=key).exists():
        me = MatchEvent(match=match, microseconds=get_microseconds(), \
            scorer=user, tower=tower, alliance=data['alliance'], \
            level=int(data['level']), collision_id=key, undo_score=data['undo_score'])
        me.save()
        update_from_match_event(me)

def finish_scoring_center(scoring_device):
    if scoring_device.on_center:
        scoring_device.on_center = False
        scoring_device.save()

def finish_scoring_match(scoring_device, match):
    tower_name = scoring_device.tower.name
    setattr(match, 'scorer_' + tower_name + '_confirmed', True)
    match.save()

def state_update(data, scoring_device):
    if data['state'] == 'no_match': return data

    data['match_number'] = 0
    try:
        match = ScoringSystem.objects.all()[0].current_match
        data['match_number'] = str(match.id)
    except:
        data['state'] = 'no_match'
        return data

    if not match.actual_start:
        data['state'] = 'prematch'
        return data
    else:
        timer = (match.actual_start + datetime.timedelta(seconds=150)) - datetime.datetime.now()
        if timer.days < 0:
            if getattr(match, 'scorer_' + data['tower_name'] + '_confirmed'):
                data['state'] = 'match_done_confirmed'
            else:
                data['state'] = 'match_done_not_confirmed'

    if data['state'] and not scoring_device.on_center: return data

    if not scoring_device.on_center:
        data['state'] = 'normal'
        return data

    center_start = getattr(match, data['tower_name'].split('_')[1] + '_center_active_start')
    try:
        diff = (center_start + datetime.timedelta(seconds=30)) - datetime.datetime.now()
        if diff.days < 0: data['state'] = 'normal_center_not_confirmed'
        else: data['state'] = 'center'
    except: data['state'] = 'normal'
    return data

@staff_member_required
def batch_actions(request):
    scoring_device = ScoringDevice.objects.get(scorer=request.user)
    scoring_device.last_contact = datetime.datetime.now()
    scoring_device.save()
    match = ScoringSystem.objects.all()[0].current_match
    if scoring_device.on_center:
        tower = Tower.objects.get(name='center')
    else:
        tower = scoring_device.tower

    actions = json.loads(request.GET.get('actions', {}))
    keys = actions.keys()
    keys.sort()
    saved_actions = []

    for key in keys:
        data = actions[key]['data']
        action = actions[key]['action']
        if action == 'score':
            score_match_event(request.user, match, tower, key, data)
        elif action == 'done_scoring_center':
            finish_scoring_center(scoring_device)
        elif action == 'done_scoring_match':
            finish_scoring_match(scoring_device, match)
        else: continue
        saved_actions.append(key)

    scorer_data = get_scorer_data(scoring_device)
    scorer_data = state_update(scorer_data, scoring_device)

    return HttpResponse(json.dumps({
            'success': True, 'action_ids':saved_actions, 'scorer_data': scorer_data,
        }), 'application/json')


# Scorekeeper Functions
@staff_member_required
def pick_scorer(request):
    group = Group.objects.get(name='Scorekeepers')
    if group not in request.user.groups.all():
        raise Http404
    match = ScoringSystem.objects.all()[0].current_match
    tower_name = request.GET.get('tower_name', '')
    scorer_id = request.GET.get('scorer_id', '')

    try:
        sd = getattr(match, 'scorer_'+tower_name).scoringdevice
        sd.tower = None
        sd.save()
    except: pass
    if str(scorer_id) == '0': setattr(match, 'scorer_'+tower_name, None)
    else: setattr(match, 'scorer_'+ tower_name +'_id', scorer_id)

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

    ss = ScoringSystem.objects.all()[0]
    match = ss.current_match
    timer = (match.actual_start + datetime.timedelta(seconds=150)) - datetime.datetime.now()
    if timer.days >= 0 and ss.task_id:
        task = abort_match.delay()
        revoke(ss.task_id, terminate=True)
    else:
        prematch_lighting()
    match.reset()
    ScoringDevice.objects.all().update(on_center=False)
    for tower_name in ['low_red', 'high_red', 'low_blue', 'high_blue']:
        setattr(match, 'scorer_'+tower_name, None)
    for sd in ScoringDevice.objects.filter(tower__isnull=False):
        setattr(match, 'scorer_'+sd.tower.name, sd.scorer)
    match.save()

    return scorekeeper(request)

@staff_member_required
def start_match(request):
    group = Group.objects.get(name='Scorekeepers')
    if group not in request.user.groups.all():
        raise Http404
    if settings.USE_CELERY:
        task = run_match.delay()
        ss = ScoringSystem.objects.all()[0]
        ss.task_id = task.task_id
        ss.save()
    else:
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
        update_from_match_event(me)
    match.calculate_scores()
    return scorekeeper(request)
