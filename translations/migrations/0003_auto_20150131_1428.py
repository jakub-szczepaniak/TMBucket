# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('translations', '0002_auto_20150128_2041'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TranslationUnit',
            new_name='TransUnit',
        ),
    ]
