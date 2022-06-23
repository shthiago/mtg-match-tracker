from django.contrib import admin

from tracker import models

from .deck import DeckAdmin
from .match import MatchAdmin

admin.site.register(models.Card)
admin.site.register(models.Deck, DeckAdmin)
admin.site.register(models.Opponent)
admin.site.register(models.OpponentDeck)
admin.site.register(models.Event)
admin.site.register(models.Match, MatchAdmin)
admin.site.register(models.Game)
admin.site.register(models.Archetype)
