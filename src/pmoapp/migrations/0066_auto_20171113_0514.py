# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-12 21:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pmoapp', '0065_plan_plan_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='plan_projResolutionTime',
            field=models.TextField(blank=True, null=True),
        ),
    ]
