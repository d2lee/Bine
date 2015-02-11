# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.', default=False)),
                ('email', models.EmailField(max_length=75, unique=True)),
                ('username', models.CharField(max_length=40, unique=True)),
                ('fullname', models.CharField(max_length=80)),
                ('birthday', models.DateField()),
                ('sex', models.CharField(max_length=1, choices=[('M', '남자'), ('F', '여자')])),
                ('tagline', models.CharField(max_length=128, blank=True)),
                ('photo', models.ImageField(upload_to='authentication/%Y/%m/%d', blank=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(to='auth.Group', verbose_name='groups', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', related_query_name='user', related_name='user_set')),
                ('user_permissions', models.ManyToManyField(to='auth.Permission', verbose_name='user permissions', blank=True, help_text='Specific permissions for this user.', related_query_name='user', related_name='user_set')),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
                'db_table': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('isbn', models.CharField(max_length=15, unique=True)),
                ('author', models.CharField(max_length=50)),
                ('illustrator', models.CharField(max_length=50, blank=True)),
                ('translator', models.CharField(max_length=50, blank=True)),
                ('publisher', models.CharField(max_length=128, blank=True)),
                ('pub_date', models.DateField(null=True, blank=True)),
                ('page', models.CharField(max_length=4, blank=True)),
                ('description', models.TextField(blank=True)),
                ('content', models.TextField(blank=True)),
                ('photo', models.ImageField(upload_to='book/%Y/%m/%d', blank=True)),
                ('language', models.CharField(max_length=2, choices=[('ko', '한국어'), ('en', '영어'), ('jp', '일어'), ('cn', '중국')], default='ko')),
                ('age_level', models.CharField(max_length=1, choices=[('1', '0-3세'), ('2', '4-7세'), ('3', '초등1-2'), ('4', '초등3-4'), ('5', '초등5-6'), ('6', '청소년'), ('7', '성인'), ('8', '유아전체'), ('9', '초등전체')], default='9')),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'books',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BookCategory',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'book_categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BookNote',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('read_date_from', models.DateField()),
                ('read_date_to', models.DateField()),
                ('content', models.TextField(blank=True)),
                ('preference', models.CharField(max_length=1, default=3)),
                ('attach', models.FileField(upload_to='notes/%Y/%m/%d', blank=True)),
                ('share_to', models.CharField(max_length=1, choices=[('P', '개인'), ('F', '친구'), ('A', '모두')], default='2')),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(to='bine.Book', related_name='booknotes')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='booknotes')),
            ],
            options={
                'db_table': 'booknotes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BookNoteReply',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('content', models.CharField(max_length=258)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('note', models.ForeignKey(to='bine.BookNote', related_name='replies')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='replies')),
            ],
            options={
                'db_table': 'booknote_replies',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='book',
            name='categories',
            field=models.ManyToManyField(to='bine.BookCategory', related_name='books'),
            preserve_default=True,
        ),
    ]
