# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('bp_cupid', '0018_praxis_related_names'),
    ]

    operations = [
        migrations.CreateModel(
            name='Platzbegrenzung',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('anzahl', models.IntegerField(validators=[django.core.validators.MinValueValidator(0, 'Anzahl darf nicht negativ sein.')], verbose_name='max. Anzahl Plätze')),
                ('praxis', models.ForeignKey(related_name='platzbegrenzung', to='bp_cupid.Praxis')),
                ('verwaltungszeitraum', models.ForeignKey(related_name='platzbegrenzung', to='bp_cupid.Verwaltungszeitraum')),
            ],
            options={
                'verbose_name_plural': 'Platzbegrenzungen',
                'verbose_name': 'Platzbegrenzung',
            },
        ),
        migrations.AlterUniqueTogether(
            name='platzbegrenzung',
            unique_together=set([('verwaltungszeitraum', 'praxis')]),
        ),
    ]
