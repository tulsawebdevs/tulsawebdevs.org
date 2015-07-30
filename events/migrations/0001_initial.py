# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
import django_pgjson.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Location Name')),
                ('address', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='Address')),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, srid=4326, null=True, verbose_name='Location')),
                ('location_hash', models.CharField(max_length=32, null=True)),
                ('meta', django_pgjson.fields.JsonField(blank=True, null=True, verbose_name='META')),
            ],
        ),
    ]
