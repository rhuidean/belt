# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-26 19:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('belt_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poke',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_poked', to='belt_app.User'),
        ),
    ]
