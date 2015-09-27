# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bp_cupid', '0011_zeitraumdaten'),
    ]

    operations = [
        migrations.CreateModel(
            name='Praxis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anrede', models.CharField(default='', blank=True, max_length=15)),
                ('vorname', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('adresse', models.CharField(blank=True, max_length=100)),
                ('plz', models.IntegerField(default=0)),
                ('ort', models.CharField(default='', blank=True, max_length=50)),
                ('telefon', models.CharField(default='', blank=True, max_length=20)),
                ('telefax', models.CharField(default='', blank=True, max_length=20)),
                ('homepage', models.URLField(default='', blank=True)),
                ('email', models.EmailField(default='', blank=True, max_length=254)),
                ('unterkunft', models.CharField(default='', blank=True, max_length=100)),
                ('lehre_bp', models.BooleanField(default=False, verbose_name='BP')),
                ('lehre_pj', models.BooleanField(default=False, verbose_name='PJ')),
                ('kinder', models.BooleanField(default=False, verbose_name='Kinder/Jugendliche')),
                ('sono', models.BooleanField(default=False, verbose_name='Sonografie')),
                ('sport', models.BooleanField(default=False, verbose_name='Sportmedizin')),
                ('kompl', models.BooleanField(default=False, verbose_name='Komplementärmedizin')),
                ('freie_unterkunft', models.BooleanField(help_text='freie Unterkunft', default=False, verbose_name='freie UK?')),
                ('billige_unterkunft', models.BooleanField(help_text='billige Unterkunft', default=False, verbose_name='billige UK?')),
                ('nur_mit_auto', models.BooleanField(help_text='nur mit Auto erreichbar?', default=False, verbose_name='nur Auto')),
                ('erg_taetigkeiten', models.TextField(blank=True, verbose_name='Ergänzungen zu den abgefragten Tätigkeitsschwerpunkten')),
                ('andere_kriterien', models.TextField(blank=True, verbose_name='andere Kriterien')),
                ('erg_unterbringung', models.TextField(blank=True, verbose_name='Ergänzungen zu den Angaben zur Unterbringung')),
                ('sonstiges', models.TextField(blank=True, verbose_name='Sonstiges')),
                ('landkreis', models.ForeignKey(null=True, to='bp_cupid.Landkreis')),
                ('zeitraeume', models.ManyToManyField(to='bp_cupid.Zeitraum', db_table='praxis_zeitraum', blank=True, verbose_name='Zeiträume')),
            ],
            options={
                'verbose_name_plural': 'Praxen',
                'verbose_name': 'Praxis',
            },
        ),
    ]
