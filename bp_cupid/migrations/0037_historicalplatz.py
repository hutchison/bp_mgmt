# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bp_cupid', '0036_aendere_hilfetext_von_vorlage'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalPlatz',
            fields=[
                ('manuell', models.BooleanField(default=False, help_text='Wenn aktiviert, dann wird der Platz bei der automatischen        Platzvergabe nicht gelöscht.')),
                ('kommentar', models.TextField(default='', blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('praxis', models.ForeignKey(related_name='+', blank=True, db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='bp_cupid.Praxis', null=True)),
                ('student', models.ForeignKey(related_name='+', blank=True, db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='bp_cupid.Student', null=True)),
                ('zeitraum', models.ForeignKey(related_name='+', blank=True, db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='bp_cupid.Zeitraum', null=True)),
            ],
            options={
                'verbose_name': 'historical Platz',
                'get_latest_by': 'history_date',
                'ordering': ('-history_date', '-history_id'),
            },
        ),
    ]
