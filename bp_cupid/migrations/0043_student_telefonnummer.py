# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('bp_cupid', '0042_evaluation'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='telefonnummer',
            field=models.CharField(validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$', message="Telefonnummer muss von folgendem Format sein: '+999999999'. Es sind bis zu 15 Ziffern erlaubt.")], max_length=15, default='', blank=True, verbose_name='Telefonnummer'),
        ),
    ]
