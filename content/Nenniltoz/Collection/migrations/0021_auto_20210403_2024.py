# Generated by Django 3.1.7 on 2021-04-04 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Collection', '0020_quickresult'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardidlist',
            name='card_url',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='quickresult',
            name='result',
            field=models.CharField(default='{}', max_length=500000),
        ),
    ]
