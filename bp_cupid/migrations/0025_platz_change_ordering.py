# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bp_cupid', '0024_praxen_aktualisiere_zeitraeume'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='platz',
            options={'ordering': ['zeitraum'], 'verbose_name': 'Platz', 'verbose_name_plural': 'Plätze'},
        ),
    ]
