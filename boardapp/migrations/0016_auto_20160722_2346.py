# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-22 20:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boardapp', '0015_notice_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genre',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='message',
            name='parent',
        ),
        migrations.DeleteModel(
            name='Genre',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]
