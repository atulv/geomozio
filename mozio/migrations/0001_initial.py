# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Zipcode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=5)),
                ('poly', django.contrib.gis.db.models.fields.PolygonField(srid=4326, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
