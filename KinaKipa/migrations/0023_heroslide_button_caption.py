# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-08 12:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KinaKipa', '0022_heroslide'),
    ]

    operations = [
        migrations.AddField(
            model_name='heroslide',
            name='button_caption',
            field=models.CharField(default='', help_text='Button caption', max_length=200, verbose_name='Button caption'),
            preserve_default=False,
        ),
    ]
