# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-02 11:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iati_organisation', '0005_auto_20160426_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budgetline',
            name='value',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=14, null=True),
        ),
        migrations.AlterField(
            model_name='recipientcountrybudget',
            name='value',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=14, null=True),
        ),
        migrations.AlterField(
            model_name='recipientorgbudget',
            name='value',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=14, null=True),
        ),
        migrations.AlterField(
            model_name='totalbudget',
            name='value',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=14, null=True),
        ),
    ]
