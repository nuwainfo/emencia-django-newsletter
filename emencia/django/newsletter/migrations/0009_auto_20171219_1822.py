# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0008_auto_20171217_0314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='subject',
            field=models.CharField(max_length=255, verbose_name='subject'),
        ),
    ]
