# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bp_cupid', '0037_historicalplatz'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalZusatzinfoPraxis',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', auto_created=True, db_index=True, blank=True)),
                ('text', models.TextField(blank=True, default='', help_text='Einfache HTML-Tags wie &lt;b&gt;, &lt;i&gt; und &lt;u&gt;funktionieren. Von weiteren Experimenten sollte man ablassen.')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL, null=True, related_name='+')),
                ('praxis', models.ForeignKey(to='bp_cupid.Praxis', related_name='+', db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, null=True, blank=True)),
                ('verwaltungszeitraum', models.ForeignKey(to='bp_cupid.Verwaltungszeitraum', related_name='+', db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'historical Zusatzinfo an Praxis',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='ZusatzinfoPraxis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('text', models.TextField(blank=True, default='', help_text='Einfache HTML-Tags wie &lt;b&gt;, &lt;i&gt; und &lt;u&gt;funktionieren. Von weiteren Experimenten sollte man ablassen.')),
                ('praxis', models.ForeignKey(to='bp_cupid.Praxis')),
                ('verwaltungszeitraum', models.ForeignKey(to='bp_cupid.Verwaltungszeitraum')),
            ],
            options={
                'verbose_name': 'Zusatzinfo an Praxis',
                'verbose_name_plural': 'Zusatzinfos an Praxen',
            },
        ),
        migrations.AlterUniqueTogether(
            name='zusatzinfopraxis',
            unique_together=set([('praxis', 'verwaltungszeitraum')]),
        ),
    ]
