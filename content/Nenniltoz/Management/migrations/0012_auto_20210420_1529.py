# Generated by Django 3.1.7 on 2021-04-20 19:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Management', '0011_auto_20210419_2020'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deckcard',
            name='card_img',
        ),
        migrations.RemoveField(
            model_name='deckcard',
            name='card_name',
        ),
        migrations.RemoveField(
            model_name='deckcard',
            name='card_search',
        ),
        migrations.AlterField(
            model_name='settings',
            name='bearer_exp',
            field=models.DateField(default=datetime.datetime(2021, 4, 20, 15, 29, 33, 954079)),
        ),
    ]
