# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone
import bine.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status', default=False)),
                ('username', models.CharField(max_length=40, unique=True)),
                ('email', models.EmailField(max_length=75, unique=True)),
                ('fullname', models.CharField(max_length=80)),
                ('birthday', models.DateField()),
                ('sex', models.CharField(choices=[('M', '남자'), ('F', '여자')], max_length=1)),
                ('tagline', models.CharField(blank=True, max_length=128)),
                ('photo', models.ImageField(upload_to='authentication/%Y/%m/%d', blank=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'users',
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('category', models.CharField(blank=True, max_length=128)),
                ('isbn', models.CharField(max_length=10, unique=True)),
                ('barcode', models.CharField(max_length=16, default='KOR0000000000000', unique=True)),
                ('author', models.CharField(max_length=50)),
                ('isbn13', models.CharField(blank=True, max_length=13)),
                ('author_etc', models.CharField(blank=True, max_length=50)),
                ('illustrator', models.CharField(blank=True, max_length=50)),
                ('translator', models.CharField(blank=True, max_length=50)),
                ('publisher', models.CharField(blank=True, max_length=128)),
                ('pub_date', models.DateField(blank=True, null=True)),
                ('page', models.CharField(blank=True, max_length=4)),
                ('description', models.TextField(blank=True)),
                ('photo', models.URLField(blank=True)),
                ('link', models.URLField(blank=True)),
                ('language', models.CharField(choices=[('ko', '한국어'), ('en', '영어'), ('jp', '일어'), ('cn', '중국')], max_length=2, default='ko')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read_date_from', models.DateField()),
                ('read_date_to', models.DateField()),
                ('content', models.TextField(blank=True)),
                ('preference', models.CharField(max_length=1, default=3)),
                ('attach', models.ImageField(upload_to=bine.models.get_file_name, null=True)),
                ('share_to', models.CharField(choices=[('P', '개인'), ('F', '친구'), ('A', '모두')], max_length=1, default='F')),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(related_name='booknotes', to='bine.Book')),
                ('user', models.ForeignKey(related_name='booknotes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'booknotes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BookNoteLikeit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('note', models.ForeignKey(related_name='likeit', to='bine.BookNote')),
                ('user', models.ForeignKey(related_name='likeit', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'booknote_likeit',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BookNoteReply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=258)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('note', models.ForeignKey(related_name='replies', to='bine.BookNote')),
                ('user', models.ForeignKey(related_name='replies', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'booknote_replies',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FriendRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('N', '대기'), ('Y', '승락'), ('D', '삭제')], max_length=1, default='N')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('from_user', models.ForeignKey(related_name='from_user', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(related_name='to_people', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'friend_relations',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='friendrelation',
            unique_together=set([('from_user', 'to_user')]),
        ),
        migrations.AlterUniqueTogether(
            name='booknotelikeit',
            unique_together=set([('user', 'note')]),
        ),
        migrations.AddField(
            model_name='user',
            name='friends',
            field=models.ManyToManyField(related_name='related_to+', to=settings.AUTH_USER_MODEL, through='bine.FriendRelation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', related_query_name='user', related_name='user_set', verbose_name='groups'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(to='auth.Permission', blank=True, help_text='Specific permissions for this user.', related_query_name='user', related_name='user_set', verbose_name='user permissions'),
            preserve_default=True,
        ),
    ]
