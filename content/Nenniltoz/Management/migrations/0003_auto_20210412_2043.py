# Generated by Django 3.1.7 on 2021-04-13 00:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Management', '0002_settings_api_set'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('color_id', models.CharField(max_length=20)),
                ('created_by', models.CharField(max_length=50, null=True)),
                ('deck_user', models.CharField(max_length=50)),
                ('is_pre_con', models.BooleanField()),
                ('is_private', models.BooleanField()),
                ('image_url', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=1000)),
                ('commander_oracle', models.CharField(max_length=200, null=True)),
                ('commander_id', models.CharField(max_length=200, null=True)),
                ('commander_name', models.CharField(max_length=200, null=True)),
                ('commander_file', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DeckType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('desc', models.CharField(max_length=50)),
                ('min_deck_size', models.IntegerField(default=60)),
                ('max_deck_size', models.IntegerField(default=0)),
                ('side_board_size', models.IntegerField(default=15)),
                ('card_copy_limit', models.IntegerField(default=4)),
                ('has_commander', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='DeckCards',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_oracle', models.CharField(max_length=200)),
                ('card_name', models.CharField(max_length=200)),
                ('card_file', models.CharField(max_length=200, null=True)),
                ('card_search', models.CharField(max_length=2000)),
                ('quantity', models.IntegerField(default=0)),
                ('sideboard', models.BooleanField(default=False)),
                ('deck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deck_cards', to='Management.deck')),
            ],
        ),
        migrations.AddField(
            model_name='deck',
            name='deck_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_deck', to='Management.decktype'),
        ),
    ]
