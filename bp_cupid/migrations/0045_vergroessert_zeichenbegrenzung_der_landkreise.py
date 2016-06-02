# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bp_cupid', '0044_zeitraum_alter_ueberlappende'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landkreis',
            name='name',
            field=models.CharField(default='', max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='landkreis',
            name='orte',
            field=models.CharField(default='', max_length=200, verbose_name='Orte'),
        ),
    ]
