# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mozio', '0003_servicearea'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicearea',
            name='provider',
            field=models.ForeignKey(default=None, to='mozio.Provider'),
            preserve_default=False,
        ),
    ]
