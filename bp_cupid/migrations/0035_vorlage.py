# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bp_cupid', '0034_site_settings'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vorlage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('token', models.SlugField(unique=True, help_text='Das Kürzel, über das die Vorlage im Code angesprochen wird.\n        Ändere dies nur, wenn du weißt, was du tust.')),
                ('text', models.TextField(default='', blank=True, help_text='Der eigentliche Text der Vorlage, der angezeigt wird.')),
            ],
            options={
                'verbose_name': 'Vorlage',
                'verbose_name_plural': 'Vorlagen',
            },
        ),
    ]
