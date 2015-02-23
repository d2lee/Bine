# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import bine.models
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', default=False, help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(unique=True, max_length=40)),
                ('email', models.EmailField(unique=True, max_length=75)),
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
                'verbose_name': 'user',
                'db_table': 'users',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=128)),
                ('isbn', models.CharField(unique=True, max_length=15)),
                ('author', models.CharField(max_length=50)),
                ('illustrator', models.CharField(blank=True, max_length=50)),
                ('translator', models.CharField(blank=True, max_length=50)),
                ('publisher', models.CharField(blank=True, max_length=128)),
                ('pub_date', models.DateField(blank=True, null=True)),
                ('page', models.CharField(blank=True, max_length=4)),
                ('description', models.TextField(blank=True)),
                ('content', models.TextField(blank=True)),
                ('photo', models.ImageField(upload_to='book/%Y/%m/%d', blank=True)),
                ('language', models.CharField(choices=[('ko', '한국어'), ('en', '영어'), ('jp', '일어'), ('cn', '중국')], default='ko', max_length=2)),
                ('age_level', models.CharField(choices=[('1', '0-3세'), ('2', '4-7세'), ('3', '초등1-2'), ('4', '초등3-4'), ('5', '초등5-6'), ('6', '청소년'), ('7', '성인'), ('8', '유아전체'), ('9', '초등전체')], default='9', max_length=1)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('read_date_from', models.DateField()),
                ('read_date_to', models.DateField()),
                ('content', models.TextField(blank=True)),
                ('preference', models.CharField(default=3, max_length=1)),
                ('attach', models.ImageField(upload_to=bine.models.get_file_name, null=True)),
                ('share_to', models.CharField(choices=[('P', '개인'), ('F', '친구'), ('A', '모두')], default='F', max_length=1)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('status', models.CharField(choices=[('N', '대기'), ('Y', '승락'), ('D', '삭제')], default='N', max_length=1)),
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
            model_name='book',
            name='categories',
            field=models.ManyToManyField(related_name='books', to='bine.BookCategory'),
            preserve_default=True,
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
            field=models.ManyToManyField(verbose_name='groups', blank=True, to='auth.Group', related_name='user_set', related_query_name='user', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(verbose_name='user permissions', blank=True, to='auth.Permission', related_name='user_set', related_query_name='user', help_text='Specific permissions for this user.'),
            preserve_default=True,
        ),
    ]
