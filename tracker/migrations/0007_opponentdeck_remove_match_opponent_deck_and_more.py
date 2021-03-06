# Generated by Django 4.0.4 on 2022-05-23 02:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0006_game_game_number_alter_game_game_notes'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpponentDeck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='match',
            name='opponent_deck',
        ),
        migrations.AddField(
            model_name='match',
            name='opponent_deck_1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='tracker.opponentdeck'),
        ),
    ]
