# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bp_cupid', '0003_landkreisdaten'),
    ]

    operations = [
        migrations.CreateModel(
            name='Verwaltungszeitraum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('anfang', models.DateField()),
                ('ende', models.DateField()),
            ],
            options={
                'verbose_name': 'Verwaltungszeitraum',
                'verbose_name_plural': 'Verwaltungszeiträume',
            },
        ),
    ]
