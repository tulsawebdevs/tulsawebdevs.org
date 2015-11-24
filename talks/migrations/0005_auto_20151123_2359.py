# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('talks', '0004_auto_20150830_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speaker',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(verbose_name='created', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='speaker',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(verbose_name='modified', auto_now=True),
        ),
        migrations.AlterField(
            model_name='talk',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(verbose_name='created', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='talk',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(verbose_name='modified', auto_now=True),
        ),
    ]
