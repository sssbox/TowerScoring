from django.http import HttpResponse, Http404#, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required
#from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import Group
#from django.forms.models import model_to_dict

from scoring.match.models import ScoringSystem, Match
#from scoring.utils.time import elapsed_time, get_microseconds

import datetime
from django.utils.timezone import now as tz_aware_now
try: import simplejson as json
except: import json

def get_timer_dict():
    match = ScoringSystem.objects.all()[0].current_match
    match_state = 'pre_match'
    try:
        timer = (match.actual_start + datetime.timedelta(seconds=151)) - tz_aware_now()
        if timer.days < 0:
            timer = '0:00'
            match_state = 'done'
        else:
            seconds = '00' + str(timer.seconds%60)
            timer = str(timer.seconds/60) + ':' + seconds[-2:]
            match_state = 'match'
    except: timer = '2:30'
    try:
        red_timer = (match.red_center_active_start + datetime.timedelta(seconds=31)) - tz_aware_now()
        if red_timer.days < 0:
            red_timer = '00'
        else:
            seconds = '00' + str(red_timer.seconds)
            red_timer = seconds[-2:]
    except: red_timer = '00'
    try:
        blue_timer = (match.blue_center_active_start + datetime.timedelta(seconds=31)) - tz_aware_now()
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
    if match.is_practice:  practice = 'Practice '
    else:  practice = ''
    response = {'timer': timer, 'blue_timer': blue_timer, 'red_timer': red_timer, \
            'match': {'red_score': red_score, 'blue_score': blue_score, 'id':match.id }, \
            'match_state':match_state, 'practice':practice, \
        }
    return response

@staff_member_required
def display(request):
    group = Group.objects.get(name='Displays')
    if group not in request.user.groups.all():
        raise Http404
    return render_to_response('display/index.html', locals())

NEXT_DISPLAY = {
        'timer': 'ranking',
        'ranking': 'timer',
#        'ranking': 'match_schedule',
#        'match_schedule': 'alliance_select',
#        'alliance_select': 'elim_bracket',
#        'elim_bracket': 'timer',
}

@staff_member_required
def update_display(request):
    group = Group.objects.get(name='Displays')
    if group not in request.user.groups.all():
        raise Http404

    du = request.user.displayuser
    display = du.display
    if request.GET.get('skip_to_screen', '') != '':
        display = request.GET.get('skip_to_screen')
        du.display = display
        du.save()
    elif request.GET.get('next_screen', 'false') == 'true':
        display = NEXT_DISPLAY[display]
        du.display = display
        du.save()
    return_dict = {'display': display }
    if display == 'timer':
        return_dict.update(get_timer_dict())

    return HttpResponse(json.dumps(return_dict), 'application/json')

