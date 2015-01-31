# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('translations', '0004_tm'),
    ]

    operations = [
        migrations.AddField(
            model_name='transunit',
            name='tm',
            field=models.ForeignKey(default=None, to='translations.TM'),
            preserve_default=True,
        ),
    ]
