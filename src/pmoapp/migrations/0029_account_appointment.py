# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-20 19:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pmoapp', '0028_auto_20171021_0217'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='appointment',
            field=models.CharField(default='Minister of Defence', max_length=150),
            preserve_default=False,
        ),
    ]
