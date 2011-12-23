from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import Group
from django.forms.models import model_to_dict

from match.models import ScoringDevice, ScoringSystem, Match
from utils.time import elapsed_time, get_microseconds

import datetime
try: import simplejson as json
except: import json

@staff_member_required
def index(request):
    group = Group.objects.get(name='Scorekeepers')
    if group in request.user.groups.all():
        return scorekeeper(request)
    group = Group.objects.get(name='Timer')
    if group in request.user.groups.all():
        return timer(request)
    return scorer(request)
    return render_to_response('index.html', locals())

@staff_member_required
def scorer(request):
    try:
        scoring_device = ScoringDevice.objects.get(scorer=request.user)
    except:
        return HttpResponse('Error, you are not set up as a scorer, contact the scorekeeper', \
                "text/plain")

    try:
        is_red = '_red' in scoring_device.tower.name
        is_low = 'low_' in scoring_device.tower.name
        if is_red:
            primary = 'red'
            non_primary = 'blue'
        else:
            primary = 'blue'
            non_primary = 'red'
    except: no_match = True
    return render_to_response('mobile_scorer/scorer.html', locals())

@staff_member_required
def timer(request, get_dict=False):
    group = Group.objects.get(name='Scorekeepers')
    if group not in request.user.groups.all():
        group = Group.objects.get(name='Timer')
        if group not in request.user.groups.all():
            raise Http404
    match = ScoringSystem.objects.all()[0].current_match
    match_state = 'pre_match'
    try:
        timer = (match.actual_start + datetime.timedelta(seconds=150)) - datetime.datetime.now()
        if timer.days < 0:
            timer = '0:00'
            match_state = 'done'
        else:
            seconds = '00' + str(timer.seconds%60)
            timer = str(timer.seconds/60) + ':' + seconds[-2:]
            match_state = 'match'
    except: timer = '2:30'
    try:
        red_timer = (match.red_center_active_start + datetime.timedelta(seconds=30)) - datetime.datetime.now()
        if red_timer.days < 0:
            red_timer = '00'
        else:
            seconds = '00' + str(red_timer.seconds)
            red_timer = seconds[-2:]
    except: red_timer = '00'
    try:
        blue_timer = (match.blue_center_active_start + datetime.timedelta(seconds=30)) - datetime.datetime.now()
        if blue_timer.days < 0:
            blue_timer = '00'
        else:
            seconds = '00' + str(blue_timer.seconds)
            blue_timer = seconds[-2:]
    except: blue_timer = '00'
    try: red_score = match.red_score
    except: red_score = 0
    try: blue_score = match.blue_score
    except: blue_score = 0
    if request.is_ajax() or get_dict:
        if match.is_practice:  practice = 'Practice'
        else:  practice = ''
        response = {'timer': timer, 'blue_timer': blue_timer, 'red_timer': red_timer, \
                'match': {'red_score': red_score, 'blue_score': blue_score, 'id':match.id }, \
                'match_state':match_state, 'practice':practice, \
            }
        if get_dict:
            return response
        return HttpResponse(json.dumps(response), 'application/json')
    return render_to_response('timer.html', locals())

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
    timer_dict = timer(request, True)
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
