# Generated by Django 3.1.7 on 2021-04-20 00:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Management', '0010_auto_20210419_1717'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deckcard',
            old_name='card_file',
            new_name='card_img',
        ),
        migrations.AlterField(
            model_name='settings',
            name='bearer_exp',
            field=models.DateField(default=datetime.datetime(2021, 4, 19, 20, 20, 8, 692771)),
        ),
    ]
