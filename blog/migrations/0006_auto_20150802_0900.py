# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20150729_1709'),
    ]

    operations = [
        migrations.AddField(
            model_name='researcherprofile',
            name='interests',
            field=models.TextField(default=' '),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 2, 8, 59, 21, 954455, tzinfo=utc)),
        ),
    ]
