# Generated by Django 3.1.7 on 2021-03-04 03:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('Collection', '0019_cardidlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardidlist',
            name='cardName',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
