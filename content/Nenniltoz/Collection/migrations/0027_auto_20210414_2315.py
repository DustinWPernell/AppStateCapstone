# Generated by Django 3.1.7 on 2021-04-15 03:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Collection', '0026_auto_20210414_2046'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardidlist',
            name='tcg_price',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cardidlist',
            name='tcg_price_date',
            field=models.DateField(default=datetime.datetime(2021, 4, 14, 23, 15, 24, 171847)),
        ),
        migrations.AlterField(
            model_name='quickresult',
            name='last_update',
            field=models.DateField(default=datetime.datetime(2021, 4, 14, 23, 15, 24, 181845)),
        ),
    ]
