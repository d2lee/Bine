# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('email', models.EmailField(max_length=75, unique=True)),
                ('username', models.CharField(max_length=40, unique=True)),
                ('fullname', models.CharField(max_length=80)),
                ('birthday', models.CharField(max_length=8)),
                ('sex', models.CharField(choices=[('M', '남자'), ('F', '여자')], max_length=1)),
                ('tagline', models.CharField(max_length=128, blank=True)),
                ('photo', models.ImageField(upload_to='authentication/%Y/%m/%d', blank=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'users',
            },
            bases=(models.Model,),
        ),
    ]
