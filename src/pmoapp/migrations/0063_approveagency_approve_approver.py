# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-11 14:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pmoapp', '0062_remove_approveagency_approve_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='approveagency',
            name='approve_approver',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='pmoapp.Account'),
            preserve_default=False,
        ),
    ]
