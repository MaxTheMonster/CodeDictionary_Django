# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-30 14:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Dictionary', '0009_auto_20170530_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Dictionary.Category'),
        ),
    ]
