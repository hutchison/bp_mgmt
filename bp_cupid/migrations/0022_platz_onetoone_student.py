# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bp_cupid', '0021_mitarbeiterdaten'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platz',
            name='student',
            field=models.OneToOneField(related_name='platz', serialize=False, primary_key=True, to='bp_cupid.Student'),
        ),
    ]
