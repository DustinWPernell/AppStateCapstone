# Generated by Django 3.1.7 on 2021-04-02 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Collection', '0018_deckcards_card_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='deckcards',
            name='card_name',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
