# Generated by Django 3.1.7 on 2021-03-14 01:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('Users', '0008_auto_20210312_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='cardView',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='deckView',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profileView',
            field=models.BooleanField(default=True),
        ),
    ]
