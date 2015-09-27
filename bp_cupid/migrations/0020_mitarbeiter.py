# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('bp_cupid', '0019_platzbegrenzung'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mitarbeiter',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('akt_verw_zeitraum', models.ForeignKey(help_text='Bei allen Ansichten werden nur Blöcke und Zeiträume des aktuellen Verwaltungszeitraums angezeigt.', verbose_name='aktueller Verwaltungszeitraum', default=1, to='bp_cupid.Verwaltungszeitraum')),
            ],
            options={
                'verbose_name_plural': 'Mitarbeiter',
                'verbose_name': 'Mitarbeiter',
            },
        ),
    ]
