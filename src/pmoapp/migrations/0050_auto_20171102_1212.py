# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-02 04:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pmoapp', '0049_auto_20171102_0106'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plan',
            old_name='plan_dateTime',
            new_name='plan_receipt',
        ),
    ]
