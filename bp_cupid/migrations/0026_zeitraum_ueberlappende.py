# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bp_cupid', '0025_platz_change_ordering'),
    ]

    operations = [
        migrations.AddField(
            model_name='zeitraum',
            name='ueberlappende',
            field=models.ManyToManyField(related_name='ueberlappende_rel_+', related_query_name='ueberlappende', blank=True, to='bp_cupid.Zeitraum', db_table='ueberlappende_zeitraeume'),
        ),
    ]
