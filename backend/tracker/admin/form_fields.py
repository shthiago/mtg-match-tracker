from typing import List, Optional, Tuple
from django import forms

from django.forms import ValidationError

from tracker.models import Card
from tracker.utils.deck_parser import DeckParser, DeckCard


class CardsField(forms.CharField):
    def __init__(self, *args, **kwargs):
        if "widget" not in kwargs:
            kwargs["widget"] = forms.Textarea()

        super().__init__(*args, **kwargs)
        self.validators.append(self.cards_validator)

    def cards_validator(self, value: str):
        parsed = self.parse(value)
        if parsed is None:
            raise ValidationError("Invalid list of cards")

        all_cardnames = [card.name for card in Card.objects.all()]

        maindeck, sideboard = parsed

        for _, cardname in maindeck + sideboard:
            if cardname not in all_cardnames:
                raise ValidationError(f"Card not found: {cardname}")

    @classmethod
    def parse(cls, value: str) -> Optional[Tuple[List[DeckCard], List[DeckCard]]]:
        return DeckParser.parse(value)
