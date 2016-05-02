# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mozio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=12)),
                ('language', models.CharField(max_length=4)),
                ('currency', models.CharField(max_length=3)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
