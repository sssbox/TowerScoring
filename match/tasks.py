from celery.decorators import task
import time, datetime

from match.models import ScoringSystem, ScoringDevice, Match, Tower, TowerLevel
from utils.time import get_microseconds
from match.tower_state import *
from utils.sound import play_sound
from utils.test_leds import update_test_led
from utils.field_leds import update_real_leds

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

def center_done(color, other_color, match):
    center = Tower.objects.get(name='center')
    low_center = center.towerlevel_set.get(level=1)
    if not getattr(match, other_color+'_center_active'):
        low_center.state = 'off'
    else:
        low_center.state = other_color
    low_center.save()
    update_test_led(low_center)
    update_real_leds(low_center)
    setattr(match, color+'_center_active', False)
    for tl in TowerLevel.objects.filter(tower__name__icontains=color):
        tl.state = 'green'
        tl.save()
        update_test_led(tl)
        update_real_leds(tl)

    match.save()

@task()
def run_match():
    locs = {}
    match_state, locs['center_red_state'], locs['center_blue_state'] = 'start', 'none', 'none'
    locs['center_red_counter_us'], locs['center_blue_counter_us'] = 0, 0
    match, us = init()
    while True:
        usdiff = get_microseconds() - us
        msdiff = round(usdiff / 1000)
        sdiff = round(msdiff / 1000)
        match = Match.objects.get(id=match.id)
        bypass = False
        if locs['center_red_state'] != 'none' and locs['center_blue_state'] != 'none':
            # if both of the timers are less than 5 seconds from the end, blink together
            if msdiff > 145000 \
                    and get_microseconds()-locs['center_red_counter_us'] > 25000000 \
                    and get_microseconds()-locs['center_blue_counter_us'] > 25000000:
                bypass = True
                color_ms_diff = round((get_microseconds() - locs['center_red_counter_us']) / 1000)
                if locs['center_red_state'] == 'on' and (color_ms_diff < 25500 \
                        or 26000 < color_ms_diff < 26500 or 27000 < color_ms_diff < 27500 \
                        or 28000 < color_ms_diff < 28500):
                    locs['center_red_state'] = 'off'
                    center = Tower.objects.get(name='center')
                    low_center = center.towerlevel_set.get(level=1)
                    low_center.state = 'off'
                    update_test_led(low_center)
                    update_real_leds(low_center)
                elif locs['center_red_state'] == 'off' and (25500 < color_ms_diff < 26000 \
                        or 26500 < color_ms_diff < 27000 or 27500 < color_ms_diff < 28000 \
                        or 28500 < color_ms_diff):
                    locs['center_red_state'] = 'on'
                    center = Tower.objects.get(name='center')
                    low_center = center.towerlevel_set.get(level=1)
                    low_center.state = 'purple'
                    update_test_led(low_center)
                    update_real_leds(low_center)
        if not bypass:
            for color, other_color in [('red', 'blue'), ('blue', 'red')]:
                if getattr(match, color+'_center_active') \
                        and locs['center_'+color+'_state'] == 'none':
                    locs['center_'+color+'_state'] = 'on'
                    this_start = get_microseconds()
                    if (us + 120000000) < this_start: #120 seconds
                        this_start = us + 120000000
                    elif locs['center_'+other_color+'_state'] != 'none':
                        other_start = locs['center_'+other_color+'_counter_us']
                        if (this_start - other_start) < 5000000:
                            this_start = other_start + 5000000
                    locs['center_'+color+'_counter_us'] = this_start
                elif locs['center_'+color+'_state'] != 'none':
                    color_ms_diff = round((get_microseconds() - locs['center_'+color \
                            +'_counter_us']) / 1000)
                    if color_ms_diff > 30000: #Done
                        center_done(color, other_color, match)
                        locs['center_'+color+'_state'] = 'none'
                    elif color_ms_diff > 25000:
                        if locs['center_'+color+'_state'] == 'on' \
                            and (color_ms_diff < 25500 \
                                or 26000 < color_ms_diff < 26500 \
                                or 27000 < color_ms_diff < 27500 \
                                or 28000 < color_ms_diff < 28500):
                            locs['center_'+color+'_state'] = 'off'
                            center = Tower.objects.get(name='center')
                            low_center = center.towerlevel_set.get(level=1)
                            if not getattr(match, other_color+'_center_active'):
                                low_center.state = 'off'
                            else:
                                low_center.state = other_color
                            update_test_led(low_center)
                            update_real_leds(low_center)
                        elif locs['center_'+color+'_state'] == 'off' \
                            and (25500 < color_ms_diff < 26000 \
                                or 26500 < color_ms_diff < 27000 \
                                or 27500 < color_ms_diff < 28000 or 28500 < color_ms_diff):
                            locs['center_'+color+'_state'] = 'on'
                            center = Tower.objects.get(name='center')
                            low_center = center.towerlevel_set.get(level=1)
                            if not getattr(match, other_color+'_center_active'):
                                low_center.state = color
                            else:
                                low_center.state = 'purple'
                            update_test_led(low_center)
                            update_real_leds(low_center)

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
    end_match_lighting()
    time.sleep(3)
    prematch_lighting()

@task()
def test_task():
    for i in range(1,60):
        print i
        time.sleep(1)

@task()
def add(x, y):
        return x + y

