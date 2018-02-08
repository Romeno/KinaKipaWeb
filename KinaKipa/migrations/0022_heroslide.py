# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-08 12:41
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('KinaKipa', '0021_auto_20180207_2052'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeroSlide',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, help_text='Hero slide image', null=True, storage=django.core.files.storage.FileSystemStorage(location='layout/image'), upload_to='', verbose_name='Hero slide image')),
                ('content', tinymce.models.HTMLField(help_text='Hero slide text', verbose_name='Hero slide text')),
                ('url', models.URLField(help_text='Url where banner will lead to', verbose_name='Url')),
            ],
        ),
    ]
