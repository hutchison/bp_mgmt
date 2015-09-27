# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bp_cupid', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Landkreis',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('plz_von', models.IntegerField(verbose_name='von', default=0)),
                ('plz_bis', models.IntegerField(verbose_name='bis', default=0)),
                ('name', models.CharField(verbose_name='Name', default='', max_length=20)),
                ('orte', models.CharField(verbose_name='Orte', default='', max_length=100)),
            ],
            options={
                'verbose_name': 'Landkreis',
                'verbose_name_plural': 'Landkreise',
            },
        ),
    ]
