# Generated by Django 3.1.6 on 2021-02-18 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='lastCardImport',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='settings',
            name='lastRuleImport',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='settings',
            name='lastSymbolImport',
            field=models.CharField(max_length=200),
        ),
    ]