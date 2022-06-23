from django import forms

from tracker.models import Deck


class DeckForm(forms.ModelForm):

    class Meta:
        model = Deck
        fields = ["owner", "name", "maindeck", "sideboard", "format"]

    owner = forms.Fore


