# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-10 20:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pmoapp', '0060_auto_20171111_0325'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notifications',
            name='PlanNum',
            field=models.IntegerField(),
        ),
    ]