import datetime
from django.db import models
from django.contrib.auth.models import User

from tournament.models import Team

class Tower(models.Model):
    NAME_CHOICES = ( \
            ('low_red', 'low_red'),
            ('high_red', 'high_red'),
            ('low_blue', 'low_blue'),
            ('high_blue', 'high_blue'),
            ('center', 'center'),
        )
    name = models.CharField(max_length=9, choices=NAME_CHOICES, unique=True)

    ALLIANCE_CHOICES = (('red', 'red'), ('blue', 'blue'), ('center', 'center'))
    alliance = models.CharField(max_length=6, choices=ALLIANCE_CHOICES)

class TowerLevel(models.Model):
    level = models.IntegerField(choices=((1, '1'), (2, '1')))
    lighting_controller_id = models.IntegerField()

    STATE_CHOICES = ( \
            ('off', 'off'),
            ('green', 'green'),
            ('red', 'red'),
            ('blue', 'blue'),
            ('purple', 'purple'),
        )
    state = models.CharField(max_length=6, choices=STATE_CHOICES)


class Match(models.Model):
    time = models.DateTimeField()
    actual_start = models.DateTimeField()

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

    scorer_low_red = models.ForeignKey(User, related_name="scoring_low_red")
    scorer_high_red = models.ForeignKey(User, related_name="scoring_high_red")
    scorer_low_blue = models.ForeignKey(User, related_name="scoring_low_blue")
    scorer_high_blue = models.ForeignKey(User, related_name="scoring_high_blue")

class MatchEvent(models.Model):
    ts = models.IntegerField()
    match = models.ForeignKey(Match)
    scorer = models.ForeignKey(User)
    team = models.CharField(max_length=4, choices=(('red', 'red'),('blue', 'blue')))
    tower = models.ForeignKey(Tower)
    LEVEL_CHOICES=((1, 'Low GV'),(2, 'High GV'),(3, 'AV'))
    level = models.IntegerField(choices=LEVEL_CHOICES)


