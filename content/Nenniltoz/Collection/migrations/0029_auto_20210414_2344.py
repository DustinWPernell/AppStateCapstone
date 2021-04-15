# Generated by Django 3.1.7 on 2021-04-15 03:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Collection', '0028_auto_20210414_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardidlist',
            name='tcg_price',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='cardidlist',
            name='tcg_price_date',
            field=models.DateField(default=datetime.datetime(2021, 4, 14, 23, 44, 51, 382631)),
        ),
        migrations.AlterField(
            model_name='quickresult',
            name='last_update',
            field=models.DateField(default=datetime.datetime(2021, 4, 14, 23, 44, 51, 386631)),
        ),
    ]
