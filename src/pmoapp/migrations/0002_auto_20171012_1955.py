# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-12 11:55
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pmoapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=15)),
                ('password', models.CharField(max_length=15)),
                ('emailAddress', models.EmailField(max_length=254)),
                ('user_type', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='CurrentReport',
            fields=[
                ('crisis_ID', models.IntegerField(validators=[django.core.validators.MaxValueValidator(9999), django.core.validators.MinValueValidator(1)])),
                ('crisis_name', models.CharField(max_length=50)),
                ('crisis_description', models.CharField(max_length=350)),
                ('crisis_dateTime', models.DateTimeField()),
                ('crisis_address', models.CharField(max_length=50)),
                ('crisis_status', models.CharField(max_length=50)),
                ('updates_curInjuries', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('updates_curDeaths', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('updates_curThreatLevel', models.CharField(max_length=50)),
                ('updates_curRadius', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('updates_curSAF', models.DecimalField(decimal_places=1, max_digits=4)),
                ('updates_curCD', models.DecimalField(decimal_places=1, max_digits=4)),
                ('updates_curSCDF', models.DecimalField(decimal_places=1, max_digits=4)),
                ('plan_ID', models.IntegerField(primary_key=True, serialize=False, validators=[django.core.validators.MaxValueValidator(99999999), django.core.validators.MinValueValidator(1)])),
                ('plan_description', models.CharField(max_length=500)),
                ('plan_status', models.CharField(max_length=50)),
                ('plan_projRadius', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('plan_projCasualtyRate', models.DecimalField(decimal_places=1, max_digits=4)),
                ('plan_projResolutionTime', models.DateTimeField()),
                ('plan_projETAResolution', models.DecimalField(decimal_places=1, max_digits=4)),
                ('plan_SAFRecommended', models.DecimalField(decimal_places=1, max_digits=4)),
                ('plan_CDRecommended', models.DecimalField(decimal_places=1, max_digits=4)),
                ('plan_SCDFRecommended', models.DecimalField(decimal_places=1, max_digits=4)),
                ('plan_SAFMaximum', models.DecimalField(decimal_places=1, max_digits=4)),
                ('plan_CDMaximum', models.DecimalField(decimal_places=1, max_digits=4)),
                ('plan_SCDFMaximum', models.DecimalField(decimal_places=1, max_digits=4)),
            ],
        ),
        migrations.DeleteModel(
            name='Crisis',
        ),
    ]