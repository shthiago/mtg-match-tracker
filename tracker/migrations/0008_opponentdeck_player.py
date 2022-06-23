# Generated by Django 4.0.4 on 2022-05-23 02:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tracker', '0007_opponentdeck_remove_match_opponent_deck_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='opponentdeck',
            name='player',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
