# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bp_cupid', '0023_praxis_freie_und_belegte_zeitraeume'),
    ]

    operations = [
        migrations.AddField(
            model_name='praxis',
            name='hat_didaktikschulung_besucht',
            field=models.BooleanField(default=False, verbose_name='hat Didaktikschulung besucht'),
        ),
        migrations.AddField(
            model_name='praxis',
            name='ist_aktiv',
            field=models.BooleanField(default=True, verbose_name='ist aktiv'),
        ),
    ]
