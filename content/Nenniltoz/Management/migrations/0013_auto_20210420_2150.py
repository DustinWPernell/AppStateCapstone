# Generated by Django 3.1.7 on 2021-04-21 01:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Management', '0012_auto_20210420_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='bearer_exp',
            field=models.DateField(default=datetime.datetime(2021, 4, 20, 21, 50, 51, 565950)),
        ),
    ]
