# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

import bine.models


class Migration(migrations.Migration):
    dependencies = [
        ('bine', '0005_auto_20150212_0644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booknote',
            name='attach',
            field=models.ImageField(null=True, upload_to=bine.models.get_file_name),
            preserve_default=True,
        ),
    ]
