# Generated by Django 3.1.6 on 2021-02-23 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Collection', '0012_cardlayout'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardlayout',
            name='sides',
            field=models.IntegerField(default=1, verbose_name=1),
            preserve_default=False,
        ),
    ]