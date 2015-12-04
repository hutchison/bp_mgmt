# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from bp_cupid.models import Zeitraum

def aktualisiere_ueberlappende_zeitraeume(apps, schema_editor):
    for zr in Zeitraum.objects.all():
        zr.aktualisiere_zeitraeume()

def entferne_ueberlappende_zeitraeume(apps, schema_editor):
    for zeitraum in Zeitraum.objects.all():
        for z in zeitraum.ueberlappende.all():
            zeitraum.ueberlappende.remove(z)

class Migration(migrations.Migration):

    dependencies = [
        ('bp_cupid', '0025_platz_change_ordering'),
    ]

    operations = [
        migrations.RunPython(
            aktualisiere_ueberlappende_zeitraeume,
            reverse_code=entferne_ueberlappende_zeitraeume
        ),
    ]
