# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-16 13:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pmoapp', '0016_auto_20171016_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='externalagency',
            name='agency_description',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
