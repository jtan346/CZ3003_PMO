# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-20 18:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pmoapp', '0027_plan_plan_submitted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='id',
        ),
        migrations.AlterField(
            model_name='account',
            name='user_type',
            field=models.CharField(max_length=15, primary_key=True, serialize=False),
        ),
    ]