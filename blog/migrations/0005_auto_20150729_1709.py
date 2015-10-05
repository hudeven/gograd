# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20150729_1627'),
    ]

    operations = [
        migrations.RenameField(
            model_name='researcherprofile',
            old_name='criticalText',
            new_name='critical_text',
        ),
        migrations.RenameField(
            model_name='researcherprofile',
            old_name='photoURL',
            new_name='photo_url',
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 29, 17, 8, 55, 912967, tzinfo=utc)),
        ),
    ]
