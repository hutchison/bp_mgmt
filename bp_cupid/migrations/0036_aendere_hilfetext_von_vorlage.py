# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bp_cupid', '0035_vorlage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vorlage',
            name='token',
            field=models.SlugField(help_text='Das Kürzel, über das die Vorlage im Code angesprochen wird.', unique=True),
        ),
    ]
