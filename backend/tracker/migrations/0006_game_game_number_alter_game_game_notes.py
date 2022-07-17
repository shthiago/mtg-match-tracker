# Generated by Django 4.0.4 on 2022-05-23 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_alter_game_game_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='game_number',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='game',
            name='game_notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]