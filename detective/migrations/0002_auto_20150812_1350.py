# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('detective', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trackinglog',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modified'),
        ),
    ]
