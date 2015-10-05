# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20150728_1132'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResearcherProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=200)),
                ('position', models.CharField(max_length=200)),
                ('university', models.CharField(max_length=200)),
                ('photoURL', models.TextField()),
                ('criticalText', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 29, 16, 27, 11, 133001, tzinfo=utc)),
        ),
    ]
