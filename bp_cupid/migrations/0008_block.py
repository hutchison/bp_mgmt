# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bp_cupid', '0007_studentendaten'),
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('verwaltungszeitraum', models.ForeignKey(related_name='bloecke', to='bp_cupid.Verwaltungszeitraum')),
            ],
            options={
                'verbose_name': 'Block',
                'verbose_name_plural': 'Blöcke',
            },
        ),
    ]
