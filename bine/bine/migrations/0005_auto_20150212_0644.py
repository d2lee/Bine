# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import bine.models


class Migration(migrations.Migration):

    dependencies = [
        ('bine', '0004_auto_20150211_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booknote',
            name='attach',
            field=models.FileField(upload_to=bine.models.get_file_name, null=True),
            preserve_default=True,
        ),
    ]
