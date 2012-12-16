from django.contrib import admin
from models import *

class DisplayUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'display', 'needs_reload')
    list_editable = ('display', 'needs_reload')

admin.site.register(DisplayUser, DisplayUserAdmin)
