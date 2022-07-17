from typing import List
from django.contrib.auth.models import User
from django.db import models

from tracker.utils.deck_parser import DeckCard


class Archetype(models.Model):
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name


class Card(models.Model):
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name

class Deck(models.Model):
    owner = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    archetype = models.ForeignKey(Archetype, on_delete=models.PROTECT, null=True)
    name = models.TextField()
    maindeck = models.ManyToManyField(
        Card, through="MaindeckPart", related_name="in_maindeck"
    )
    sideboard = models.ManyToManyField(
        Card, through="SideboardPart", related_name="in_sideboard"
    )
    FORMATS = [
        ("M", "Modern"),
        ("P", "Pioneer"),
        ("L", "Legacy"),
    ]
    format = models.TextField(choices=FORMATS)

    def __str__(self):
        return self.name

    def as_plaintext(self) -> str:
        maindeck = [
            f"{p.copies} {p.card.name}"
            for p in self.maindeck.through.objects.filter(deck=self)
        ]
        sideboard = [
            f"SB: {p.copies} {p.card.name}"
            for p in self.sideboard.through.objects.filter(deck=self)
        ]

        return "\n".join(maindeck + sideboard)

    def update_maindeck(self, cards: List[DeckCard]):
        self._update_cards(self.maindeck, cards)

    def update_sideboard(self, cards: List[DeckCard]):
        self._update_cards(self.sideboard, cards)

    def _update_cards(self, manager: models.ManyToManyField, cards: List[DeckCard]):
        new_entries = []
        for copies, cardname in cards:
            card = Card.objects.filter(name=cardname).first()

            if not card:
                raise Exception(f"Card  not found: {cardname}")

            new_entries.append((copies, card))

        manager.clear()
        for copies, card in new_entries:
            manager.add(card, through_defaults={"copies": copies})


class MaindeckPart(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.PROTECT)
    card = models.ForeignKey(Card, on_delete=models.PROTECT)
    copies = models.IntegerField()


class SideboardPart(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.PROTECT)
    card = models.ForeignKey(Card, on_delete=models.PROTECT)
    copies = models.IntegerField()


class Opponent(models.Model):
    player = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.TextField()

    def __str__(self):
        return self.name


class OpponentDeck(models.Model):
    player = models.ForeignKey(User, on_delete=models.PROTECT)
    archetype = models.ForeignKey(Archetype, on_delete=models.PROTECT)

    def __str__(self):
        return self.archetype.name


class Event(models.Model):
    name = models.TextField()
    date = models.DateField()

    def __str__(self):
        return f"{self.name} on {self.date}"


class Match(models.Model):
    player = models.ForeignKey(User, on_delete=models.PROTECT)
    player_deck = models.ForeignKey(
        Deck, on_delete=models.PROTECT, related_name="as_player"
    )
    opponent = models.ForeignKey(Opponent, on_delete=models.PROTECT)
    opponent_deck = models.ForeignKey(OpponentDeck, on_delete=models.PROTECT)

    event = models.ForeignKey(Event, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.player.username} vs {self.opponent.name} at {self.event}"


class Game(models.Model):
    match = models.ForeignKey(Match, on_delete=models.PROTECT)
    player_win = models.BooleanField()
    player_mulligans = models.IntegerField(default=0)
    opponent_mulligans = models.IntegerField(default=0)
    game_notes = models.TextField(null=True, blank=True)
    game_number = models.IntegerField(
        choices=[(1, "G1"), (2, "G2"), (3, "G3"), (4, "G4"), (5, "G5")]
    )

    def __str__(self):
        return f"[{'X' if self.player_win else ' '}] Game {self.game_number} of {self.match}"
