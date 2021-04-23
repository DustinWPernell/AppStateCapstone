# Generated by Django 3.1.7 on 2021-04-23 00:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Management', '0013_auto_20210420_2150'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deck',
            name='commander_file',
        ),
        migrations.RemoveField(
            model_name='deck',
            name='commander_id',
        ),
        migrations.RemoveField(
            model_name='deck',
            name='commander_name',
        ),
        migrations.RemoveField(
            model_name='deck',
            name='commander_oracle',
        ),
        migrations.AddField(
            model_name='deck',
            name='card_list',
            field=models.CharField(default='', max_length=2000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deck',
            name='side_list',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='settings',
            name='bearer_exp',
            field=models.DateField(default=datetime.datetime(2021, 4, 22, 20, 11, 25, 126281)),
        ),
    ]
