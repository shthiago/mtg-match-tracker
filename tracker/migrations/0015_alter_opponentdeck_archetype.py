# Generated by Django 4.0.4 on 2022-06-07 01:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0014_rename__archetype_opponentdeck_archetype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opponentdeck',
            name='archetype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tracker.archetype'),
        ),
    ]
