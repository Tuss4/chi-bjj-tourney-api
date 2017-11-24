# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-24 18:46
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('usrtoken', '0002_auto_20161129_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confirmationtoken',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 26, 18, 46, 47, 20274, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='passwordtoken',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 26, 18, 46, 47, 20274, tzinfo=utc)),
        ),
    ]