# Generated by Django 3.1.7 on 2021-03-27 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Collection', '0011_cardface_image_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='deck',
            name='deck_user',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
