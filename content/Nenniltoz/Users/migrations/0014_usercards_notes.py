# Generated by Django 3.1.7 on 2021-03-23 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0013_auto_20210319_1953'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercards',
            name='notes',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]