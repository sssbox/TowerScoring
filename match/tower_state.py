from match.models import TowerLevel
from utils.test_leds import update_test_led
from utils.field_leds import update_real_leds

def prematch_lighting():
    #TODO center tower alternate at 1s intervals?
    TowerLevel.objects.filter(tower__name__icontains='red').update(state='red')
    TowerLevel.objects.filter(tower__name__icontains='blue').update(state='blue')
    TowerLevel.objects.filter(tower__name='center', level=1).update(state='red')
    TowerLevel.objects.filter(tower__name='center', level=2).update(state='blue')
    for tl in TowerLevel.objects.all():
        update_test_led(tl)
        update_real_leds(tl)

# Dry run means it is only clearing the internal state in order to figure out the score
# after a match event was deleted.
def start_match_lighting(dry_run_only=False):
    TowerLevel.objects.filter(tower__name__icontains='_').update(state='green')
    TowerLevel.objects.filter(tower__name='center', level=1).update(state='off')
    TowerLevel.objects.filter(tower__name='center', level=2).update(state='green')

    if not dry_run_only:
        for tl in TowerLevel.objects.all():
            update_test_led(tl)
            update_real_leds(tl)

def end_match_lighting():
    #turn off all lights
    TowerLevel.objects.all().update(state='off')
    for tl in TowerLevel.objects.all():
        update_test_led(tl)
        update_real_leds(tl)
