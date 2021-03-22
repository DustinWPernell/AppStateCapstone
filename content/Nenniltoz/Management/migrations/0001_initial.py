# Generated by Django 3.1.7 on 2021-03-20 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_card_import', models.CharField(max_length=200)),
                ('last_rule_import', models.CharField(max_length=200)),
                ('last_symbol_import', models.CharField(max_length=200)),
                ('api_bulk_data', models.CharField(max_length=200)),
                ('api_card', models.CharField(max_length=200)),
                ('api_symbol', models.CharField(max_length=200)),
                ('api_rule', models.CharField(max_length=200)),
                ('api_sing_card', models.CharField(max_length=200)),
            ],
        ),
    ]
