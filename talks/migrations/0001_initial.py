# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Speaker',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created', django_extensions.db.fields.CreationDateTimeField(verbose_name='created', editable=False, blank=True, default=django.utils.timezone.now)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(verbose_name='modified', editable=False, blank=True, default=django.utils.timezone.now)),
                ('name', models.CharField(null=True, max_length=60, verbose_name='Name', blank=True, unique=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, verbose_name='Name Slug', populate_from='name')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, blank=True, null=True, verbose_name='User')),
            ],
            options={
                'abstract': False,
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='Talk',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created', django_extensions.db.fields.CreationDateTimeField(verbose_name='created', editable=False, blank=True, default=django.utils.timezone.now)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(verbose_name='modified', editable=False, blank=True, default=django.utils.timezone.now)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, verbose_name='slug', populate_from='title')),
                ('accepted', models.BooleanField(default=False)),
                ('speaker', models.ForeignKey(to='talks.Speaker', blank=True, null=True)),
            ],
            options={
                'abstract': False,
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
            },
        ),
    ]
