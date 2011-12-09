import datetime

from django.contrib.admin.views.decorators import staff_member_required
from models import *

def get_microseconds():
    now = datetime.datetime.now()
    ms = now.microsecond
    ms += now.second * 1000000
    ms += now.minute * 60000000
    ms += now.hour * 3600000000
    return ms


# inputs POSTed:
# alliance = red or blue -- alliance who scored on the goal
# level = 1, 2 or 3 ( 1 low gv (or only gv), 2 high gv, 3 av score)
@staff_member_required
def score_event(request):
    scoring_device = ScoringDevice.objects.get(scorer=request.user)
    now = datetime.datetime.now()
    match = ScoringSystem.objects.all()[0]
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
    # TODO update scoring.
