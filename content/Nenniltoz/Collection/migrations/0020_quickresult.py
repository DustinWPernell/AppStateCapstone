# Generated by Django 3.1.7 on 2021-04-03 02:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Collection', '0019_deckcards_card_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuickResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search', models.CharField(max_length=500)),
                ('last_update', models.DateField(default=datetime.datetime.now)),
                ('result', models.CharField(max_length=500000)),
            ],
        ),
    ]
