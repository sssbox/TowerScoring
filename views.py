from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import Group

from match.models import ScoringDevice, ScoringSystem

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
    return render_to_response('scorer.html', locals())

@staff_member_required
def scorekeeper(request):
    try: ss = ScoringSystem.objects.all()[0]
    except:
        ss = ScoringSystem()
        ss.save()
    try: match = ss.current_match
    except: match = None
    sd_avail = ScoringDevice.objects.filter(tower__isnull=True)
    towers = {}
    for sd in ScoringDevice.objects.filter(tower__isnull=False):
        try:
            if 'high_blue'==sd.tower.name: confirmed = match.scorer_high_blue_confirmed
            elif 'high_red'==sd.tower.name: confirmed = match.scorer_high_red_confirmed
            elif 'low_blue'==sd.tower.name: confirmed = match.scorer_low_blue_confirmed
            elif 'low_red'==sd.tower.name: confirmed = match.scorer_low_red_confirmed
        except: confirmed = False
        towers[sd.tower.name] = sd.get_stats(confirmed)
    return render_to_response('scorekeeper/scorekeeper.html', locals())

@staff_member_required
def timer(request):
    match = ScoringSystem.objects.all()[0].current_match
    try:
        timer = (match.actual_start + datetime.timedelta(seconds=150)) - datetime.datetime.now()
        if timer.days < 0:
            timer = '0:00'
        else:
            seconds = '00' + str(timer.seconds%60)
            timer = str(timer.seconds/60) + ':' + seconds[-2:]
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
    if request.is_ajax():
        response = {'timer': timer, 'blue_timer': blue_timer, 'red_timer': red_timer, \
                'match': {'red_score': red_score, 'blue_score': blue_score}
            }
        return HttpResponse(json.dumps(response), 'application/json')
    return render_to_response('timer.html', locals())

def test_ajax(request):
    return HttpResponse('{"success":true}', 'application/json')
