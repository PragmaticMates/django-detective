# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TrackingLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('request_method', models.CharField(max_length=16, verbose_name='request method')),
                ('ip_address', models.GenericIPAddressField(default=None, null=True, verbose_name='IP address', blank=True)),
                ('path', models.CharField(max_length=1024, verbose_name='path')),
                ('params_get', models.TextField(verbose_name='GET params')),
                ('params_post', models.TextField(verbose_name='POST params')),
                ('session', models.TextField(verbose_name='session')),
                ('status_code', models.SmallIntegerField(verbose_name='status code')),
                ('language_code', models.CharField(default=None, max_length=2, null=True, verbose_name='language code', blank=True)),
                ('timezone', models.CharField(default=None, max_length=128, null=True, verbose_name='timezone', blank=True)),
                ('content_type', models.CharField(default=None, max_length=128, null=True, verbose_name='content type', blank=True)),
                ('user_agent', models.CharField(default=None, max_length=1024, null=True, verbose_name='user agent', blank=True)),
                ('response', models.TextField(default=None, null=True, verbose_name='response', blank=True)),
                ('is_secure', models.BooleanField(verbose_name='secure')),
                ('is_ajax', models.BooleanField(verbose_name='ajax')),
                ('is_debug', models.BooleanField(verbose_name='debug')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='created')),
                ('user', models.ForeignKey(default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='user')),
            ],
            options={
                'ordering': ('-created',),
                'db_table': 'detective_trackinglogs',
                'verbose_name': 'tracking log',
                'verbose_name_plural': 'tracking logs',
            },
        ),
    ]
