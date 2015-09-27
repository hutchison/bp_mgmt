# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bp_cupid', '0030_besondere_praxen_unterkunftsinformationen'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='abgeneigte_praxen',
            field=models.ManyToManyField(db_table='abgeneigte_praxen', blank=True, related_name='abgeneigte_praxen', to='bp_cupid.Praxis'),
        ),
        migrations.AddField(
            model_name='student',
            name='besondere_praxiskriterien',
            field=models.TextField(blank=True, verbose_name='besondere Praxiskriterien', default=''),
        ),
        migrations.AddField(
            model_name='student',
            name='bevorzugte_praxen',
            field=models.ManyToManyField(db_table='bevorzugte_praxen', blank=True, related_name='bevorzugte_praxen', to='bp_cupid.Praxis'),
        ),
        migrations.AlterField(
            model_name='student',
            name='hat_fragebogen_ausgefuellt',
            field=models.BooleanField(verbose_name='hat Fragebogen ausgefüllt', default=False),
        ),
    ]
