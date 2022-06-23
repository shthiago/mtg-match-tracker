from typing import Any
from django.contrib import admin
from django import forms
from tracker.models import Deck

from .form_fields import CardsField


class DeckForm(forms.ModelForm):
    maindeck = CardsField()
    sideboard = CardsField()

    class Meta:
        model = Deck
        fields = "__all__"


class DeckAdmin(admin.ModelAdmin):
    form = DeckForm

    class Meta:
        model = Deck
        fields = ["owner", "name", "maindeck", "sideboard", "format"]
