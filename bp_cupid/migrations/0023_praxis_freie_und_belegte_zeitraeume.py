# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bp_cupid', '0022_platz_onetoone_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='praxis',
            name='belegte_zeitraeume',
            field=models.ManyToManyField(to='bp_cupid.Zeitraum', blank=True, db_table='praxis_zeitraum_belegt', verbose_name='belegte Zeiträume', related_name='praxen_belegt'),
        ),
        migrations.AddField(
            model_name='praxis',
            name='freie_zeitraeume',
            field=models.ManyToManyField(to='bp_cupid.Zeitraum', blank=True, db_table='praxis_zeitraum_frei', verbose_name='freie Zeiträume', related_name='praxen_frei'),
        ),
    ]
