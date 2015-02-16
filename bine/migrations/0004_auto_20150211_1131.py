# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        ('bine', '0003_booknote_likeit'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookNoteLikeit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('note', models.ForeignKey(related_name='likeit', to='bine.BookNote')),
                ('user', models.ForeignKey(related_name='likeit', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'booknote_likeit',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='booknotelikeit',
            unique_together=set([('user', 'note')]),
        ),
        migrations.RemoveField(
            model_name='booknote',
            name='likeit',
        ),
    ]
