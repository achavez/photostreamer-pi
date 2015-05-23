# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('photo', models.ImageField(upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('full_sent', models.BooleanField()),
                ('full_sent_at', models.DateTimeField(blank=True, null=True)),
                ('thumb_sent', models.BooleanField()),
                ('thumb_sent_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
