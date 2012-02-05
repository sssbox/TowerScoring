from celery.decorators import task
import time, datetime

from match.models import ScoringSystem, ScoringDevice, Match
from utils.time import get_microseconds
from match.tower_state import *
from utils.sound import play_sound

def init():
    play_sound('start')
    match = ScoringSystem.objects.all()[0].current_match
    match.reset()
    ScoringDevice.objects.all().update(on_center=False)
    match.actual_start = datetime.datetime.now()
    match.save()
    start_match_lighting()
    us = get_microseconds()
    return match, us

@task()
def run_match():
    match, us = init()
#    while True:
#        match = Match.objects.get(id=match.id)
    time.sleep(5)

@task()
def test_task():
    for i in range(1,60):
        print i
        time.sleep(1)
