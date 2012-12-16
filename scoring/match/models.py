from django.utils.timezone import now as tz_aware_now
from django.db import models
from django.contrib.auth.models import User, Group

from scoring.display.models import DisplayUser
from scoring.tournament.models import Team
from scoring.utils.time import elapsed_time, get_microseconds
SCORE_SETTINGS = { \
        1: 5,
        2: 10,
        3: 20,
    }

ALLIANCE_CHOICES = (('red', 'red'), ('blue', 'blue'), ('center', 'center'))
class Tower(models.Model):
    TOWER_CHOICES = ( \
            ('low_red', 'low_red'),
            ('high_red', 'high_red'),
            ('low_blue', 'low_blue'),
            ('high_blue', 'high_blue'),
            ('center', 'center'),
        )
    name = models.CharField(max_length=9, choices=TOWER_CHOICES, unique=True)

#    alliance = models.CharField(max_length=6, choices=ALLIANCE_CHOICES)
    def __unicode__(self):
        return self.name

class TowerLevel(models.Model):
    tower = models.ForeignKey(Tower)
    level = models.IntegerField(choices=((1, '1'), (2, '2')))
    lighting_controller_id = models.IntegerField()

    STATE_CHOICES = ( \
            ('off', 'off'),
            ('green', 'green'),
            ('red', 'red'),
            ('blue', 'blue'),
            ('purple', 'purple'),
        )
    state = models.CharField(max_length=6, choices=STATE_CHOICES)

    class Meta:
        unique_together = ('tower', 'level')

    def __unicode__(self):
        return str(self.tower) + ' ring ' + str(self.level)

class Match(models.Model):
    is_practice = models.BooleanField(default=False)
    time = models.DateTimeField()
    actual_start = models.DateTimeField(null=True, blank=True)

    red_1 = models.ForeignKey(Team, related_name="as_red_1")
    red_2 = models.ForeignKey(Team, related_name="as_red_2")
    blue_1 = models.ForeignKey(Team, related_name="as_blue_1")
    blue_2 = models.ForeignKey(Team, related_name="as_blue_2")

    red_1_gv_present = models.BooleanField(default=False)
    red_1_av_present = models.BooleanField(default=False)
    red_2_gv_present = models.BooleanField(default=False)
    red_2_av_present = models.BooleanField(default=False)
    blue_1_gv_present = models.BooleanField(default=False)
    blue_1_av_present = models.BooleanField(default=False)
    blue_2_gv_present = models.BooleanField(default=False)
    blue_2_av_present = models.BooleanField(default=False)

    red_score = models.IntegerField(default=0)
    blue_score = models.IntegerField(default=0)
    red_score_pre_penalty = models.IntegerField(default=0)
    blue_score_pre_penalty = models.IntegerField(default=0)
    red_penalties = models.IntegerField(default=0)
    blue_penalties = models.IntegerField(default=0)
    red_bonus = models.IntegerField(default=0)
    blue_bonus = models.IntegerField(default=0)

    blue_center_active = models.BooleanField(default=False)
    red_center_active = models.BooleanField(default=False)

    blue_center_active_start = models.DateTimeField(null=True, blank=True)
    red_center_active_start = models.DateTimeField(null=True, blank=True)

    scorer_low_red = models.ForeignKey(User, related_name="scoring_low_red", null=True, blank=True)
    scorer_low_red_confirmed = models.BooleanField(default=False)
    scorer_high_red = models.ForeignKey(User, related_name="scoring_high_red", null=True, blank=True)
    scorer_high_red_confirmed = models.BooleanField(default=False)
    scorer_low_blue = models.ForeignKey(User, related_name="scoring_low_blue", null=True, blank=True)
    scorer_low_blue_confirmed = models.BooleanField(default=False)
    scorer_high_blue = models.ForeignKey(User, related_name="scoring_high_blue", null=True, blank=True)
    scorer_high_blue_confirmed = models.BooleanField(default=False)

    def calculate_scores(self):
        self.red_score = self.red_score_pre_penalty + self.red_bonus - self.red_penalties
        self.blue_score = self.blue_score_pre_penalty + self.blue_bonus - self.blue_penalties
        self.save()

    def reset_score(self):
        self.red_score = 0
        self.blue_score = 0
        self.red_score_pre_penalty = 0
        self.blue_score_pre_penalty = 0
        self.save()

    def reset(self):
        self.reset_score()
        self.actual_start = None
        self.matchevent_set.all().delete()
        self.red_penalties = 0
        self.blue_penalties = 0
        self.red_bonus = 0
        self.blue_bonus = 0
        self.red_center_active = False
        self.blue_center_active = False
        self.red_center_active_start = None
        self.blue_center_active_start = None
        self.scorer_low_red_confirmed = False
        self.scorer_high_red_confirmed = False
        self.scorer_low_blue_confirmed = False
        self.scorer_high_blue_confirmed = False
        self.save()

    def __unicode__(self):
        return 'Match ' + str(self.id)

    def get_alliances(self):
        alliances = {'red':{'team_1':{}, 'team_2':{}}, 'blue':{'team_1':{}, 'team_2':{}}}
        alliances['red']['team_1']['t'] = self.red_1
        alliances['red']['team_1']['av'] = self.red_1_av_present
        alliances['red']['team_1']['gv'] = self.red_1_gv_present
        alliances['red']['team_2']['t'] = self.red_2
        alliances['red']['team_2']['av'] = self.red_2_av_present
        alliances['red']['team_2']['gv'] = self.red_2_gv_present
        alliances['blue']['team_1']['t'] = self.blue_1
        alliances['blue']['team_1']['av'] = self.blue_1_av_present
        alliances['blue']['team_1']['gv'] = self.blue_1_gv_present
        alliances['blue']['team_2']['t'] = self.blue_2
        alliances['blue']['team_2']['av'] = self.blue_2_av_present
        alliances['blue']['team_2']['gv'] = self.blue_2_gv_present
        return alliances

class ScoringDevice(models.Model):
    scorer = models.OneToOneField(User)
    tower = models.OneToOneField(Tower, blank=True, null=True)

    #Set automatically to True based on state of match, set manually to False after center not active and done scoring center.
    on_center = models.BooleanField(default=False)
    last_contact = models.DateTimeField(auto_now_add=True)
    is_lefty = models.BooleanField(default=False)
    needs_reload = models.BooleanField(default=False)

    def __unicode__(self):
        try:  return str(self.scorer) + ' scoring ' + str(self.tower)
        except:  return str(self.scorer)

    def get_stats(self, confirmed):
        stats = {}
        stats['scorer'] = self.scorer.username
        stats['scorer_id'] = self.scorer.id
        stats['confirmed'] = confirmed
        diff = tz_aware_now() - self.last_contact
        stats['last_contact'] = elapsed_time(diff.seconds, separator=', ')
        try:
            diff = get_microseconds()-self.scorer.matchevent_set.all().latest('id').microseconds
            stats['last_event'] = elapsed_time(diff/1000000, separator=', ')
        except: stats['last_event'] = 'N/A'
        return stats

class ScoringSystem(models.Model):
    current_match = models.ForeignKey(Match, blank=True, null=True)
    task_id = models.CharField(max_length=100, blank=True)

class MatchEvent(models.Model):
    match = models.ForeignKey(Match)
    microseconds = models.BigIntegerField()
    scorer = models.ForeignKey(User)
    tower = models.ForeignKey(Tower)
    alliance = models.CharField(max_length=6, choices=ALLIANCE_CHOICES)
    LEVEL_CHOICES=((1, 'Low GV'),(2, 'High GV'),(3, 'AV'))
    level = models.IntegerField(choices=LEVEL_CHOICES)
    collision_id = models.IntegerField()
    undo_score = models.BooleanField(default=False)
    dud = models.BooleanField(default=False)

    class Meta:
        unique_together = ('scorer', 'collision_id')
        ordering = ['-id']

def create_user_types_from_groups(sender, instance, created, **kwargs):
    group, _ = Group.objects.get_or_create(name='Scorers')
    if group in instance.groups.all():
        sd, _ = ScoringDevice.objects.get_or_create(scorer=instance)
    group, _ = Group.objects.get_or_create(name='Displays')
    if group in instance.groups.all():
        tu, _ = DisplayUser.objects.get_or_create(user=instance)

models.signals.post_save.connect(create_user_types_from_groups, sender=User)

