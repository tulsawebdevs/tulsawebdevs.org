# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='Location Name', max_length=255)),
                ('address', models.CharField(verbose_name='Address', max_length=255, unique=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(verbose_name='Location', blank=True, null=True, srid=4326)),
            ],
        ),
    ]
