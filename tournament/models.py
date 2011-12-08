from django.db import models

class Team(models.Model):
    number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    school = models.CharField(max_length=100)
    sponsors = models.CharField(max_length=255)
    av_name = models.CharField(max_length=100, blank=True)
    have_av = models.BooleanField(default=True)
    gv_name = models.CharField(max_length=100, blank=True)
    have_gv = models.BooleanField(default=True)
