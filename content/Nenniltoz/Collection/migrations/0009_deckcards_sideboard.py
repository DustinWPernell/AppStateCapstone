# Generated by Django 3.1.7 on 2021-03-25 01:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('Collection', '0008_auto_20210323_2314'),
    ]

    operations = [
        migrations.AddField(
            model_name='deckcards',
            name='sideboard',
            field=models.BooleanField(default=False),
        ),
    ]
