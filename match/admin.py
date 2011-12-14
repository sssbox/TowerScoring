from django.contrib import admin
from models import *

class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'red_1', 'red_2', 'blue_1', 'blue_2', 'red_score', 'blue_score',)

class ScoringDeviceAdmin(admin.ModelAdmin):
    list_display = ('scorer', 'tower', )

class MatchEventAdmin(admin.ModelAdmin):
    list_display = ('match', 'scorer', 'tower', 'alliance', 'level')
    list_filter = ('match', )

admin.site.register(Match, MatchAdmin)
admin.site.register(ScoringDevice, ScoringDeviceAdmin)
admin.site.register(MatchEvent, MatchEventAdmin)
