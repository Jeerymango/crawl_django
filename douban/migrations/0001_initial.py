# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-04-19 11:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('top', models.CharField(max_length=4)),
                ('name', models.CharField(max_length=128)),
                ('director', models.CharField(max_length=256)),
                ('time', models.CharField(max_length=128)),
                ('country', models.CharField(max_length=128)),
                ('style', models.CharField(max_length=128)),
                ('mark', models.CharField(max_length=10)),
            ],
        ),
    ]
