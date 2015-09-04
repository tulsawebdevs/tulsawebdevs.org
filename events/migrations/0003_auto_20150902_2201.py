# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20150815_1837'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventcategory',
            options={'ordering': ('lft',), 'verbose_name_plural': 'Event Categories', 'verbose_name': 'Event Category'},
        ),
    ]
