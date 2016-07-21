# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-20 14:21
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('boardapp', '0003_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 7, 20, 14, 21, 44, 272662, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='genre',
            name='updated',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 7, 20, 14, 21, 59, 793343, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(default=None, max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='genre',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='boardapp.Genre'),
        ),
    ]