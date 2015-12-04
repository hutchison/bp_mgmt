# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.core.management import call_command


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0001_initial'),
        ('auth', '0001_initial'),
        ('actstream', '0001_initial'),
    ]

    operations = []
