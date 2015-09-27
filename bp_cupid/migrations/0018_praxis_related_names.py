# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bp_cupid', '0017_block_unique'),
    ]

    operations = [
        migrations.AlterField(
            model_name='praxis',
            name='landkreis',
            field=models.ForeignKey(related_name='praxen', null=True, to='bp_cupid.Landkreis'),
        ),
        migrations.AlterField(
            model_name='praxis',
            name='zeitraeume',
            field=models.ManyToManyField(verbose_name='Zeiträume', db_table='praxis_zeitraum', related_name='praxen', blank=True, to='bp_cupid.Zeitraum'),
        ),
    ]
