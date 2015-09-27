# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bp_cupid', '0028_student_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='hat_fragebogen_ausgefuellt',
            field=models.BooleanField(default=False),
        ),
    ]
