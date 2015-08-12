# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
import recurrence.fields
import django.utils.timezone
import mptt.fields
import django_pgjson.fields
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', django_extensions.db.fields.CreationDateTimeField(editable=False, blank=True, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(editable=False, blank=True, default=django.utils.timezone.now, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('slug', django_extensions.db.fields.AutoSlugField(editable=False, blank=True, populate_from='title', verbose_name='slug')),
                ('start', models.DateTimeField(verbose_name='Start time')),
                ('end', models.DateTimeField(verbose_name='End time')),
                ('recurrences', recurrence.fields.RecurrenceField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EventCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('slug', django_extensions.db.fields.AutoSlugField(editable=False, blank=True, populate_from='name', verbose_name='Slug')),
                ('order', models.PositiveSmallIntegerField(default=0)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', null=True, blank=True, to='events.EventCategory', verbose_name='Parent')),
            ],
            options={
                'ordering': ('lft',),
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Location Name')),
                ('address', models.CharField(max_length=255, blank=True, null=True, unique=True, verbose_name='Address')),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326, blank=True, null=True, verbose_name='Location')),
                ('location_hash', models.CharField(max_length=32, null=True)),
                ('meta', django_pgjson.fields.JsonField(blank=True, null=True, verbose_name='metadata')),
            ],
        ),
        migrations.CreateModel(
            name='Occurrence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', django_extensions.db.fields.CreationDateTimeField(editable=False, blank=True, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(editable=False, blank=True, default=django.utils.timezone.now, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('slug', django_extensions.db.fields.AutoSlugField(editable=False, blank=True, populate_from='title', verbose_name='slug')),
                ('start', models.DateTimeField(verbose_name='Start time')),
                ('end', models.DateTimeField(verbose_name='End time')),
                ('original_start', models.DateTimeField(verbose_name='Original start')),
                ('original_end', models.DateTimeField(verbose_name='Original end')),
                ('cancelled', models.BooleanField(default=False, verbose_name='Cancelled')),
                ('event', models.ForeignKey(related_name='occurrences', to='events.Event', verbose_name='Event')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='event',
            name='category',
            field=models.ForeignKey(related_name='events', null=True, blank=True, to='events.EventCategory', verbose_name='Category'),
        ),
    ]
