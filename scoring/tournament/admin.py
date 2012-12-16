from django.contrib import admin
from models import *

class TeamAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'location', 'av_name', 'gv_name', 'match_points', 'highest_match_points',)

admin.site.register(Team, TeamAdmin)
