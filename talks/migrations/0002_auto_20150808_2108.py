# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('talks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speaker',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(editable=False, verbose_name='Slug', populate_from='name', blank=True),
        ),
    ]
