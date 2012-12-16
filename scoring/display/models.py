from django.db import models
from django.contrib.auth.models import User

class DisplayUser(models.Model):
    user = models.OneToOneField(User)
    DISPLAY_CHOICES = (
            ('timer', 'Timer'),
            ('ranking', 'Ranking'),
            ('match_schedule', 'Match Schedule (TODO)'),
            ('alliance_select', 'Alliance Selection (TODO)'),
            ('elim_bracket', 'Elimination Bracket (TODO)'),
        )
    display = models.CharField(max_length=20, default='timer', choices=DISPLAY_CHOICES)
    needs_reload = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.user) + ' Showing: ' + self.display

