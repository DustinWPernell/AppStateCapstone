# Generated by Django 3.1.7 on 2021-03-21 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Collection', '0004_auto_20210321_1449'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cardface',
            name='card_id',
        ),
        migrations.RemoveField(
            model_name='cardface',
            name='oracle_id',
        ),
        migrations.RemoveField(
            model_name='legality',
            name='oracle_id',
        ),
        migrations.AlterField(
            model_name='legality',
            name='brawl',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='legality',
            name='commander',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='legality',
            name='duel',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='legality',
            name='future',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='legality',
            name='gladiator',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='legality',
            name='historic',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='legality',
            name='legacy',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='legality',
            name='modern',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='legality',
            name='old_school',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='legality',
            name='pauper',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='legality',
            name='penny',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='legality',
            name='premodern',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='legality',
            name='standard',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='legality',
            name='vintage',
            field=models.CharField(max_length=30),
        ),
    ]
