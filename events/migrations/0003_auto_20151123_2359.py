# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20150815_1837'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventcategory',
            options={'ordering': ('lft',), 'verbose_name': 'Event Category', 'verbose_name_plural': 'Event Categories'},
        ),
        migrations.AlterField(
            model_name='event',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(verbose_name='created', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(verbose_name='modified', auto_now=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(verbose_name='created', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(verbose_name='modified', auto_now=True),
        ),
    ]
