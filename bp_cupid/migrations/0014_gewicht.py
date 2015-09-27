# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bp_cupid', '0013_praxendaten'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gewicht',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('wert', models.FloatField()),
                ('kommentar', models.TextField(default='', blank=True)),
                ('praxis', models.ForeignKey(to='bp_cupid.Praxis', related_name='gewichte')),
                ('student', models.ForeignKey(to='bp_cupid.Student', related_name='gewichte')),
            ],
            options={
                'verbose_name_plural': 'Gewichte',
                'verbose_name': 'Gewicht',
            },
        ),
        migrations.AlterUniqueTogether(
            name='gewicht',
            unique_together=set([('student', 'praxis')]),
        ),
    ]
