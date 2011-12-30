from django.db import models

class Team(models.Model):
    number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    school = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    sponsors = models.CharField(max_length=255)
    av_name = models.CharField(max_length=100, blank=True)
    have_av = models.BooleanField(default=True)
    gv_name = models.CharField(max_length=100, blank=True)
    have_gv = models.BooleanField(default=True)

    match_points = models.IntegerField(default=0)
    highest_match_points = models.IntegerField(default=0)

    def update_points(self):
        self.match_points = 0
        self.highest_match_points = 0
        # TODO double check that we want (as coded) highest_match_points to be attendance based.
        for match in self.as_red_1.all():
            this_score = 0
            if match.red_1_av_present: this_score += match.red_score
            if match.red_1_gv_present: this_score += match.red_score
            self.match_points += this_score
            self.highest_match_points = max(self.highest_match_points, this_score)
        for match in self.as_red_2.all():
            this_score = 0
            if match.red_2_av_present: this_score += match.red_score
            if match.red_2_gv_present: this_score += match.red_score
            self.match_points += this_score
            self.highest_match_points = max(self.highest_match_points, this_score)
        for match in self.as_blue_1.all():
            this_score = 0
            if match.blue_1_av_present: this_score += match.blue_score
            if match.blue_1_gv_present: this_score += match.blue_score
            self.match_points += this_score
            self.highest_match_points = max(self.highest_match_points, this_score)
        for match in self.as_blue_2.all():
            this_score = 0
            if match.blue_2_av_present: this_score += match.blue_score
            if match.blue_2_gv_present: this_score += match.blue_score
            self.match_points += this_score
            self.highest_match_points = max(self.highest_match_points, this_score)
        self.save()

    def __unicode__(self):
        return str(self.number) + ' - ' + self.name
