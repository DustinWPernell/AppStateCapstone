# Generated by Django 3.1.7 on 2021-03-13 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Collection', '0020_cardidlist_cardname'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='color',
            field=models.CharField(default='{C}', max_length=30),
            preserve_default=False,
        ),
    ]
