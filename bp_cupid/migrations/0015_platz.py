# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bp_cupid', '0014_gewicht'),
    ]

    operations = [
        migrations.CreateModel(
            name='Platz',
            fields=[
                ('student', models.ForeignKey(to='bp_cupid.Student', related_name='platz', serialize=False, primary_key=True)),
                ('manuell', models.BooleanField(default=False, help_text='Wenn aktiviert, dann wird der Platz bei der automatischen        Platzvergabe nicht gelöscht.')),
                ('kommentar', models.TextField(blank=True, default='')),
                ('praxis', models.ForeignKey(related_name='plaetze', to='bp_cupid.Praxis')),
                ('zeitraum', models.ForeignKey(related_name='plaetze', to='bp_cupid.Zeitraum')),
            ],
            options={
                'verbose_name': 'Platz',
                'verbose_name_plural': 'Plätze',
            },
        ),
        migrations.AlterUniqueTogether(
            name='platz',
            unique_together=set([('praxis', 'zeitraum')]),
        ),
    ]
