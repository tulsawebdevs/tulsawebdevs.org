# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('talks', '0002_auto_20150808_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speaker',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(verbose_name='Slug', blank=True, populate_from='get_name', editable=False),
        ),
        migrations.AlterField(
            model_name='talk',
            name='speaker',
            field=models.ForeignKey(null=True, blank=True, related_name='talks', to='talks.Speaker'),
        ),
    ]
