# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bp_cupid', '0009_blockdaten'),
    ]

    operations = [
        migrations.CreateModel(
            name='Zeitraum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('anfang', models.DateField()),
                ('ende', models.DateField()),
                ('block', models.ForeignKey(related_name='zeitraeume', to='bp_cupid.Block')),
            ],
            options={
                'verbose_name': 'Zeitraum',
                'ordering': ['anfang'],
                'verbose_name_plural': 'Zeiträume',
            },
        ),
        migrations.AddField(
            model_name='zeitraum',
            name='ueberlappende',
            field=models.ManyToManyField(related_name='ueberlappende_rel_+', related_query_name='ueberlappende', blank=True, to='bp_cupid.Zeitraum', db_table='ueberlappende_zeitraeume'),
        ),
    ]
