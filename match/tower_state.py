from match.models import TowerLevel

def prematch_lighting():
    #TODO center tower alternate at 1s intervals?
    TowerLevel.objects.filter(tower__name__icontains='red').update(state='red')
    TowerLevel.objects.filter(tower__name__icontains='blue').update(state='blue')
    TowerLevel.objects.filter(tower__name='center', level=1).update(state='red')
    TowerLevel.objects.filter(tower__name='center', level=2).update(state='blue')

# Dry run means it is only clearing the internal state in order to figure out the score
# after a match event was deleted.
def start_match_lighting(dry_run_only=False):
    # towers all green
    # top center ring green
    # bottom center ring off
    TowerLevel.objects.filter(tower__name__icontains='_').update(state='green')
    TowerLevel.objects.filter(tower__name='center', level=1).update(state='green')
    TowerLevel.objects.filter(tower__name='center', level=2).update(state='off')

    if not dry_run_only:
        pass #TODO here goes the actual code to update the field lighting.

def end_match_lighting():
    #turn off all lights
    TowerLevel.objects.all().update(state='off')
