# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-20 19:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pmoapp', '0029_account_appointment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evalplan',
            name='eval_text',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
