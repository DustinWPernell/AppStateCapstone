# Generated by Django 3.1.7 on 2021-04-15 00:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Management', '0004_auto_20210413_2110'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='bearer',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='settings',
            name='bearer_exp',
            field=models.DateField(default=datetime.datetime(2021, 4, 14, 20, 46, 19, 935973)),
        ),
    ]
