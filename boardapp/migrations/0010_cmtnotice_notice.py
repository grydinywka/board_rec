# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-21 06:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boardapp', '0009_cmtnotice_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='cmtnotice',
            name='notice',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='boardapp.Notice'),
        ),
    ]
