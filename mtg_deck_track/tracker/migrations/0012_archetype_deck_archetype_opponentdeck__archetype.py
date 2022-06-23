# Generated by Django 4.0.4 on 2022-06-07 01:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0011_rename_name_opponentdeck_archetype_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Archetype',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='deck',
            name='archetype',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='tracker.archetype'),
        ),
        migrations.AddField(
            model_name='opponentdeck',
            name='_archetype',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='tracker.archetype'),
        ),
    ]
