from django.contrib import admin
from django import forms
from tracker.models import Deck

from tracker.admin.form_fields import CardsField
from tracker.utils.deck_parser import DeckParser


class DeckForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        instance = kwargs["instance"]
        self.fields["decklist"].initial = instance.as_plaintext()

    decklist = CardsField()

    class Meta:
        model = Deck
        fields = ("owner", "archetype", "name", "format", "decklist")

    def save(self, commit: bool):
        initial_cards = self.fields["decklist"].initial
        form_cards = self.cleaned_data["decklist"]
        if initial_cards != form_cards:
            maindeck, sideboard = DeckParser.parse(self.cleaned_data["decklist"])
            deck: Deck = self.instance
            deck.update_maindeck(maindeck)
            deck.update_sideboard(sideboard)

        return super().save(commit)


class DeckAdmin(admin.ModelAdmin):
    form = DeckForm
