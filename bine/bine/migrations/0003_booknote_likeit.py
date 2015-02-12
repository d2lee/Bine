# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bine', '0002_auto_20150209_1214'),
    ]

    operations = [
        migrations.AddField(
            model_name='booknote',
            name='likeit',
            field=models.SmallIntegerField(default=0),
            preserve_default=True,
        ),
    ]
