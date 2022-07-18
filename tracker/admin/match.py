from django.contrib import admin
from django.forms import ModelForm
from tracker.models import Match, Game


class GameInlineForm(ModelForm):
    class Meta:
        model = Game
        fields = (
            "match",
            "player_win",
            "player_mulligans",
            "opponent_mulligans",
            "game_notes",
            "game_number",
        )


class GameInline(admin.StackedInline):
    model = Game
    form = GameInlineForm

    verbose_name_plural = "Games"
    extra = 0
    fk_name = "match"


class MatchAdmin(admin.ModelAdmin):
    class Meta:
        model = Match

    inlines = (GameInline,)
