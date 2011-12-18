import datetime
from django.db import models
from django.contrib.auth.models import User

from tournament.models import Team

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

    def __unicode__(self):
        return 'Match ' + str(self.id)

class ScoringDevice(models.Model):
    scorer = models.ForeignKey(User)
    tower = models.ForeignKey(Tower)

    #Set automatically to True based on state of match, set manually to False after center not active and done scoring center.
    on_center = models.BooleanField(default=False)

class ScoringSystem(models.Model):
    current_match = models.ForeignKey(Match)

class MatchEvent(models.Model):
    match = models.ForeignKey(Match)
    microseconds = models.BigIntegerField()
    scorer = models.ForeignKey(User)
    tower = models.ForeignKey(Tower)
    alliance = models.CharField(max_length=6, choices=ALLIANCE_CHOICES)
    LEVEL_CHOICES=((1, 'Low GV'),(2, 'High GV'),(3, 'AV'))
    level = models.IntegerField(choices=LEVEL_CHOICES)
