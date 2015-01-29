# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('translations', '0003_tm'),
    ]

    operations = [
        migrations.AddField(
            model_name='translationunit',
            name='tm',
            field=models.ForeignKey(to='translations.TM', default=None),
            preserve_default=True,
        ),
    ]
