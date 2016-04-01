# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bp_cupid', '0043_student_telefonnummer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zeitraum',
            name='ueberlappende',
            field=models.ManyToManyField(to='bp_cupid.Zeitraum', db_table='ueberlappende_zeitraeume', related_name='_zeitraum_ueberlappende_+', blank=True),
        ),
    ]
