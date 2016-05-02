# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mozio', '0004_servicearea_provider'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Zipcode',
        ),
        migrations.AlterField(
            model_name='provider',
            name='email',
            field=models.EmailField(unique=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='provider',
            name='name',
            field=models.CharField(max_length=255, db_index=True),
        ),
        migrations.AlterField(
            model_name='provider',
            name='phone',
            field=models.CharField(max_length=12, db_index=True),
        ),
        migrations.AlterField(
            model_name='servicearea',
            name='name',
            field=models.CharField(max_length=255, db_index=True),
        ),
        migrations.AlterUniqueTogether(
            name='servicearea',
            unique_together=set([('provider', 'name')]),
        ),
    ]
