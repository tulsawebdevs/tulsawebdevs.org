# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ('start',)},
        ),
        migrations.AlterModelOptions(
            name='occurrence',
            options={'ordering': ('start',)},
        ),
        migrations.AddField(
            model_name='event',
            name='description_template',
            field=models.TextField(null=True, blank=True, help_text='jinja2 template used to render occurrence descriptions'),
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.ForeignKey(blank=True, null=True, to='events.Location'),
        ),
        migrations.AddField(
            model_name='event',
            name='title_template',
            field=models.TextField(null=True, blank=True, help_text='jinja2 template used to render occurrence titles'),
        ),
        migrations.AddField(
            model_name='occurrence',
            name='location',
            field=models.ForeignKey(blank=True, null=True, to='events.Location'),
        ),
    ]
