# Generated by Django 3.1.7 on 2021-04-15 00:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Collection', '0025_auto_20210413_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quickresult',
            name='last_update',
            field=models.DateField(default=datetime.datetime(2021, 4, 14, 20, 46, 19, 923973)),
        ),
    ]
