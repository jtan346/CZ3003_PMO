# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-16 14:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pmoapp', '0019_auto_20171016_2213'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='approveagency',
            name='approve_agency',
        ),
        migrations.RemoveField(
            model_name='approveagency',
            name='approve_plan',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='plan_extAgencies',
        ),
        migrations.DeleteModel(
            name='ApproveAgency',
        ),
    ]