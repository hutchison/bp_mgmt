# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bp_cupid', '0016_platzdaten'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='block',
            unique_together=set([('name', 'verwaltungszeitraum')]),
        ),
    ]
