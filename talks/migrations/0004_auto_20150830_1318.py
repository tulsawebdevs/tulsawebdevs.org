# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('talks', '0003_auto_20150816_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speaker',
            name='name',
            field=models.CharField(max_length=60, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='speaker',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(editable=False, populate_from='name', blank=True, verbose_name='Slug'),
        ),
    ]
