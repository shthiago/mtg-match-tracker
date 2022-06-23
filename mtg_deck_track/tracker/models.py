from django.contrib.auth.models import User
from django.db import models


class Archetype(models.Model):
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name


class Card(models.Model):
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name


class CardListManyToManyField(models.ManyToManyField):
    def value_from_object(self, obj):
        if obj.pk is None:
            return []

        manager = getattr(obj, self.attname)

        parts = manager.through.objects.filter(deck_id=obj.id)

        return [(part.copies, part.card) for part in parts]

    def save_form_data(self, deck: "Deck", data: str) -> None:
        manager = getattr(deck, self.attname)
        new_entries = []
        for row in data.split("\n"):

            stripped = row.strip()
            if len(stripped) == 0:
                continue

            copies, cardname = stripped.split(" ", maxsplit=1)
            copies = int(copies)
            card = Card.objects.filter(name=cardname).first()

            if not card:
                raise Exception(f"Card  not found: {cardname}")

            new_entries.append((copies, card))

        manager.clear()
        for copies, card in new_entries:
            manager.add(card, through_defaults={"copies": copies})


class Deck(models.Model):
    owner = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    archetype = models.ForeignKey(Archetype, on_delete=models.PROTECT, null=True)
    name = models.TextField()
    maindeck = CardListManyToManyField(
        Card, through="MaindeckPart", related_name="in_maindeck"
    )
    sideboard = CardListManyToManyField(
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
    player_mulligans = models.IntegerField()
    opponent_mulligans = models.IntegerField()
    game_notes = models.TextField(null=True, blank=True)
    game_number = models.IntegerField()

    def __str__(self):
        return f"[{'X' if self.player_win else ' '}] Game {self.game_number} of {self.match}"
