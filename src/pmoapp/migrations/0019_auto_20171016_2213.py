# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-16 14:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pmoapp', '0018_auto_20171016_2141'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='approveagency',
            options={'verbose_name_plural': 'Agency Approval'},
        ),
        migrations.RemoveField(
            model_name='approveagency',
            name='approve_approval',
        ),
    ]
