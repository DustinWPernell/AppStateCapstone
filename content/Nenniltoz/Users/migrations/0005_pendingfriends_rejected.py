# Generated by Django 3.1.7 on 2021-02-26 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0004_pendingfriends'),
    ]

    operations = [
        migrations.AddField(
            model_name='pendingfriends',
            name='rejected',
            field=models.BooleanField(default=False),
        ),
    ]
