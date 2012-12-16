from scoring.match.models import TowerLevel
from scoring.utils.test_leds import update_test_led
from scoring.utils.field_leds import update_real_leds

def change_led_set(tls, color=None):
    for tl in tls:
        if color:
            tl.state = color
        update_test_led(tl)
        update_real_leds(tl)

def prematch_lighting():
    #TODO center tower alternate at 1s intervals?
    change_led_set(TowerLevel.objects.filter(tower__name__icontains='red'), 'red')
    change_led_set(TowerLevel.objects.filter(tower__name__icontains='blue'), 'blue')
    change_led_set(TowerLevel.objects.filter(tower__name='center', level=1), 'red')
    change_led_set(TowerLevel.objects.filter(tower__name='center', level=2), 'blue')

# Dry run means it is only clearing the internal state in order to figure out the score
# after a match event was deleted.
def start_match_lighting(dry_run_only=False):
    TowerLevel.objects.filter(tower__name__icontains='_').update(state='green')
    TowerLevel.objects.filter(tower__name='center', level=1).update(state='off')
    TowerLevel.objects.filter(tower__name='center', level=2).update(state='green')

    if not dry_run_only:
        change_led_set(TowerLevel.objects.all())

def end_match_lighting():
    #turn off all lights
    change_led_set(TowerLevel.objects.all(), 'off')
    for tl in TowerLevel.objects.all():
        tl.state = 'off'
        update_test_led(tl)
        update_real_leds(tl)
