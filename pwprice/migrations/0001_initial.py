# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NgFilter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ng_1', models.TextField(verbose_name='NG Wards 1', blank=True)),
                ('ng_2', models.TextField(verbose_name='NG Wards 2', blank=True)),
            ],
            options={
                'verbose_name': 'NG\u30ef\u30fc\u30c9\u30fb\u5e83\u544a\u7ba1\u7406',
            },
        ),
    ]
