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

def end_match():
    end_match_lighting()
    play_sound('end')
    time.sleep(5)
    prematch_lighting()

def end_game():
    play_sound('warning')

@task()
def run_match():
    match_state, center_red_state, center_blue_state = 'start', 'off', 'off'
    match, us = init()
    while True:
        usdiff = get_microseconds() - us
        msdiff = round(usdiff / 1000)
        sdiff = round(msdiff / 1000)
        match = Match.objects.get(id=match.id)
        if match_state != 'end_game' and msdiff > 120000:# last 30 seconds
            match_state = 'end_game'
            end_game()

        if msdiff > 150000:
            end_match()
            return
        time.sleep(0.05)

@task()
def abort_match():
    play_sound('abort')
    time.sleep(3)

@task()
def test_task():
    for i in range(1,60):
        print i
        time.sleep(1)
