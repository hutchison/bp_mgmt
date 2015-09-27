# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bp_cupid', '0005_verwaltungszeitraumdaten'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('mat_nr', models.IntegerField(verbose_name='Matrikelnummer', unique=True)),
                ('name', models.CharField(verbose_name='Name', default='', max_length=50, blank=True)),
                ('vorname', models.CharField(verbose_name='Vorname', default='', max_length=100, blank=True)),
                ('email', models.EmailField(verbose_name='E-Mail', default='', max_length=254)),
                ('weiblich', models.BooleanField(default=False)),
                ('kinder', models.BooleanField(verbose_name='Kinder', default=False)),
                ('gewichtung_kinder', models.IntegerField(verbose_name='G Kinder', default=0)),
                ('sono', models.BooleanField(verbose_name='Sono', default=False)),
                ('gewichtung_sono', models.IntegerField(verbose_name='G Sono', default=0)),
                ('sport', models.BooleanField(verbose_name='Sport', default=False)),
                ('gewichtung_sport', models.IntegerField(verbose_name='G Sport', default=0)),
                ('kompl', models.BooleanField(verbose_name='Kompl', default=False)),
                ('gewichtung_kompl', models.IntegerField(verbose_name='G Kompl', default=0)),
                ('hohe_duene', models.BooleanField(verbose_name='H. Düne', default=False)),
                ('gewichtung_hohe_duene', models.IntegerField(verbose_name='G H. Düne', default=0)),
                ('entfernte_praxis_wenn_unterkunft', models.BooleanField(verbose_name='entf. Praxis', default=False)),
                ('fs_und_fahrzeug', models.BooleanField(verbose_name='FS+Auto', default=False)),
                ('priv_unterkunft', models.BooleanField(verbose_name='priv. Unterkunft', default=False)),
                ('adresse_priv_unterkunft', models.TextField(verbose_name='Ort+PLZ', default='', max_length=300, blank=True)),
                ('sonstiges', models.TextField(verbose_name='Sonstiges', default='', max_length=500, blank=True)),
                ('extern', models.BooleanField(verbose_name='macht BP extern', default=False)),
                ('landkreise', models.ManyToManyField(db_table='student_landkreis', to='bp_cupid.Landkreis', blank=True)),
                ('verwaltungszeitraum', models.ForeignKey(to='bp_cupid.Verwaltungszeitraum')),
            ],
            options={
                'verbose_name': 'Student',
                'ordering': ['name', 'mat_nr'],
                'verbose_name_plural': 'Studenten',
            },
        ),
    ]
