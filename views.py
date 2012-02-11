from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import Group
from django.forms.models import model_to_dict

from match.models import ScoringDevice, ScoringSystem, Match, MatchEvent
from utils.time import elapsed_time, get_microseconds
from display.views import display, get_timer_dict

import datetime
try: import simplejson as json
except: import json

@staff_member_required
def index(request):
    group = Group.objects.get(name='Scorekeepers')
    if group in request.user.groups.all():
        return scorekeeper(request)
    group = Group.objects.get(name='Displays')
    if group in request.user.groups.all():
        return display(request)
    return scorer(request)

def get_scorer_data(scoring_device):
    data = {'state': '', 'is_red': '', 'is_low': '', 'primary':'', 'non_primary':''}
    try:
        data['tower_name'] = scoring_device.tower.name
        data['is_red'] = '_red' in data['tower_name']
        data['is_low'] = 'low_' in data['tower_name']
    except: data['state'] = 'no_match'
    return data

@staff_member_required
def scorer(request):
    try:
        scoring_device = ScoringDevice.objects.get(scorer=request.user)
    except:
        return HttpResponse('Error, you are not set up as a scorer, contact the scorekeeper', \
                "text/plain")

    try: next_id = MatchEvent.objects.filter(scorer=request.user).order_by('-collision_id')[0].collision_id + 1
    except: next_id = 1

    data = get_scorer_data(scoring_device)

    locs = locals()
    locs.update(data)
    del locs['data']
    locs['no_match'] = locs['state'] == 'no_match'
    return render_to_response('mobile_scorer/scorer.html', locs)

@staff_member_required
def scorekeeper(request):
    group = Group.objects.get(name='Scorekeepers')
    if group not in request.user.groups.all():
        raise Http404
    del(group)
    try: ss = ScoringSystem.objects.all()[0]
    except:
        ss = ScoringSystem()
        ss.save()
    try:
        match = ss.current_match
        alliances = match.get_alliances()
    except: match = None
    timer_dict = get_timer_dict()
    sd_avail = ScoringDevice.objects.filter(tower__isnull=True)
    towers = {}
    if timer_dict['match_state'] != 'pre_match':
        try:towers['low_red'] = ScoringDevice.objects.get(scorer=match.scorer_low_red).get_stats(match.scorer_low_red_confirmed)
        except:
            try: diff = get_microseconds() - match.scorer_low_red.match_event_set.all().latest('id').microseconds
            except: diff = 0
            try:
                towers['low_red'] = {'scorer':match.scorer_low_red.username, \
                    'confirmed':match.scorer_low_red_confirmed, 'last_contact': 'N/A', \
                    'last_event': elapsed_time(diff/100000, separator=', ')}
            except: pass
        try: towers['high_red'] = ScoringDevice.objects.get(scorer=match.scorer_high_red).get_stats(match.scorer_high_red_confirmed)
        except:
            try: diff = get_microseconds() - match.scorer_high_red.scorer.match_event_set.all().latest('id').microseconds
            except: diff = 0
            try:
                towers['high_red'] = {'scorer':match.scorer_high_red.username, \
                    'confirmed':match.scorer_high_red_confirmed, 'last_contact': 'N/A', \
                    'last_event': elapsed_time(diff/100000, separator=', ')}
            except: pass
        try: towers['low_blue'] = ScoringDevice.objects.get(scorer=match.scorer_low_blue).get_stats(match.scorer_low_blue_confirmed)
        except:
            try: diff = get_microseconds() - match.scorer_low_blue.match_event_set.all().latest('id').microseconds
            except: diff = 0
            try:
                towers['low_blue'] = {'scorer':match.scorer_low_blue.username, \
                    'confirmed':match.scorer_low_blue_confirmed, 'last_contact': 'N/A', \
                    'last_event': elapsed_time(diff/100000, separator=', ')}
            except: pass
        try: towers['high_blue'] = ScoringDevice.objects.get(scorer=match.scorer_high_blue).get_stats(match.scorer_high_blue_confirmed)
        except:
            try: diff = get_microseconds() - match.scorer_high_blue.match_event_set.all().latest('id').microseconds
            except: diff = 0
            try:
                towers['high_blue'] = {'scorer':match.scorer_high_blue.username, \
                    'confirmed':match.scorer_high_blue_confirmed, 'last_contact': 'N/A', \
                    'last_event': elapsed_time(diff/100000, separator=', ')}
            except: pass
    else:
        for sd in ScoringDevice.objects.filter(tower__isnull=False):
            try:
                if 'high_blue'==sd.tower.name: confirmed = match.scorer_high_blue_confirmed
                elif 'high_red'==sd.tower.name: confirmed = match.scorer_high_red_confirmed
                elif 'low_blue'==sd.tower.name: confirmed = match.scorer_low_blue_confirmed
                elif 'low_red'==sd.tower.name: confirmed = match.scorer_low_red_confirmed
            except: confirmed = False
            towers[sd.tower.name] = sd.get_stats(confirmed)
        try:del(sd)
        except: pass
        try:del(confirmed)
        except: pass
    matches = Match.objects.all()
    del(ss)
    if request.is_ajax():
        sd_avail_list = []
        for sd in sd_avail:
            sd_avail_list.append({'id': sd.scorer.id, 'username': sd.scorer.username })
        try: del(sd)
        except: pass
        del(sd_avail)
        del(matches)
        del(request)
        locs = locals()
        locs['match'] = model_to_dict(match)
        locs['match']['match_events'] = []
        for event in match.matchevent_set.all().order_by('id'):
            event_dict = model_to_dict(event)
            event_dict['scorer'] = model_to_dict(event.scorer, fields=('id', 'username'))
            event_dict['tower'] = model_to_dict(event.tower)
            locs['match']['match_events'].append(event_dict)
        f=('name', 'number')
        locs['alliances']['blue']['team_1']['t'] = model_to_dict(alliances['blue']['team_1']['t'],fields=f)
        locs['alliances']['blue']['team_2']['t'] = model_to_dict(alliances['blue']['team_2']['t'],fields=f)
        locs['alliances']['red']['team_1']['t'] = model_to_dict(alliances['red']['team_1']['t'], fields=f)
        locs['alliances']['red']['team_2']['t'] = model_to_dict(alliances['red']['team_2']['t'], fields=f)
        del(locs['match']['actual_start'])
        del(locs['match']['time'])
        del(locs['match']['red_center_active_start'])
        del(locs['match']['blue_center_active_start'])
        return HttpResponse(json.dumps(locs), 'application/json')

    del(request)
    return render_to_response('scorekeeper/scorekeeper.html', locals())

def test_ajax(request):
    return HttpResponse('{"success":true}', 'application/json')

def logout(request):
    django_logout(request)
    return HttpResponseRedirect('/')
