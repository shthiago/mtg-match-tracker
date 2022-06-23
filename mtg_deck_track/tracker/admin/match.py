from django.contrib import admin
from tracker.models import Match


class MatchAdmin(admin.ModelAdmin):
    class Meta:
        model = Match
