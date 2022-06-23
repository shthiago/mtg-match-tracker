import json

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from loguru import logger

from tracker.models import Card


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("json_file")

    def handle(self, *_, **options):
        with open(options["json_file"]) as f:
            data = json.load(f)["data"]

        for card in data:
            try:
                Card.objects.create(name=card)
            except IntegrityError:
                logger.warning(f"Skipping duplicated card: {card}")
