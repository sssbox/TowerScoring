from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import Group

from match.models import ScoringDevice

@staff_member_required
def index(request):
    group = Group.objects.get(name='Scorekeepers')
    if group in request.user.groups.all():
        return scorekeeper(request)
    return scorer(request)
    return render_to_response('index.html', locals())

@staff_member_required
def scorer(request):
    try:
        scoring_device = ScoringDevice.objects.get(scorer=request.user)
    except:
        return HttpResponse('Error, you are not set up as a scorer, contact the scorekeeper', \
                "text/plain")

    is_red = '_red' in scoring_device.tower.name
    is_low = 'low_' in scoring_device.tower.name
    if is_red:
        primary = 'red'
        non_primary = 'blue'
    else:
        primary = 'blue'
        non_primary = 'red'
    return render_to_response('scorer.html', locals())

@staff_member_required
def scorekeeper(request):
    return render_to_response('scorekeeper.html', locals())

def test_ajax(request):
    return HttpResponse('{"success":true}', 'application/json')
