# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-20 07:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pmoapp', '0024_evalplan'),
    ]

    operations = [
        migrations.AddField(
            model_name='evalplan',
            name='eval_hasComment',
            field=models.BooleanField(default=False),
        ),
    ]
