# Generated by Django 3.1.7 on 2021-03-29 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0023_auto_20210324_2352'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar_file',
            field=models.ImageField(null=True, upload_to='static/img/avatars'),
        ),
    ]
