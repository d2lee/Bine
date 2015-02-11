# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bine', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booknote',
            name='attach',
            field=models.FileField(null=True, upload_to='notes/%Y/%m/%d'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='booknote',
            name='share_to',
            field=models.CharField(default='F', choices=[('P', '개인'), ('F', '친구'), ('A', '모두')], max_length=1),
            preserve_default=True,
        ),
    ]
