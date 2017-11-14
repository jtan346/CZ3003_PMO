# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-14 04:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pmoapp', '0071_merge_20171114_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='plan_agencies',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='username',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='plan',
            name='plan_status',
            field=models.CharField(max_length=200),
        ),
    ]
