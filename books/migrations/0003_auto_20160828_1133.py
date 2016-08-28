# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-28 10:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20160828_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookborrow',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
