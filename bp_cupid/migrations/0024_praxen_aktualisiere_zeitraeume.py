# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from bp_cupid.models import Praxis

def aktualisiere_zeitraeume_von_praxen(apps, schema_editor):
    for p in Praxis.objects.all():
        p.aktualisiere_zeitraeume()

def entferne_freie_und_belegte_zeitraeume(apps, schema_editor):
    for p in Praxis.objects.all():
        for zr in p.freie_zeitraeume.all():
            p.freie_zeitraeume.remove(zr)
        for zr in p.belegte_zeitraeume.all():
            p.belegte_zeitraeume.remove(zr)

class Migration(migrations.Migration):

    dependencies = [
        ('bp_cupid', '0023a_praxen_aktiv_didaktikschulung'),
    ]

    operations = [
        migrations.RunPython(
            aktualisiere_zeitraeume_von_praxen,
            reverse_code=entferne_freie_und_belegte_zeitraeume
        ),
    ]
