import re
from typing import List
from django import forms

from django.forms import ValidationError, fields

from tracker.models import Card


def cards_validator(value: str):
    rgx = r"((\d{1,2} .*)|\n)*"
    if re.fullmatch(rgx, value) is None:
        raise ValidationError("Invalid list of cards")

    all_cardnames = [card.name for card in Card.objects.all()]

    for row in value.split("\n"):
        if not row.strip():
            continue

        _, cardname = row.split(" ", maxsplit=1)
        if cardname.strip() not in all_cardnames:
            raise ValidationError(f"Card not found: {cardname}")


class CardsArea(forms.Textarea):
    def render(self, name: str, value: List[Card], attrs, renderer) -> str:
        if isinstance(value, list):
            rows = []
            for count, card in value:
                rows.append(f"{count} {card.name}")

            value = "\n".join(rows)

        return super().render(name, value, attrs, renderer)


class CardsField(fields.CharField):
    def __init__(self, *args, **kwargs):
        if "widget" not in kwargs:
            kwargs["widget"] = CardsArea()

        super().__init__(*args, **kwargs)
        self.validators.append(cards_validator)
