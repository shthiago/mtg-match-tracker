# Generated by Django 4.0.4 on 2022-05-23 02:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("tracker", "0008_opponentdeck_player"),
    ]

    operations = [migrations.RenameField("match", "opponent_deck_1", "opponent_deck")]
