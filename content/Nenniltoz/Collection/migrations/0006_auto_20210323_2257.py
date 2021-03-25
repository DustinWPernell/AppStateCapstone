# Generated by Django 3.1.7 on 2021-03-24 02:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Collection', '0005_auto_20210321_1820'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('colorId', models.CharField(max_length=20)),
                ('createdBy', models.CharField(max_length=20, null=True)),
                ('isPreCon', models.BooleanField()),
                ('isPrivate', models.BooleanField()),
                ('imageURL', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=1000)),
                ('commander', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='commander_deck', to='Collection.cardface')),
            ],
        ),
        migrations.CreateModel(
            name='DeckType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('desc', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='DeckCards',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='face_cards', to='Collection.cardface')),
                ('deck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deck_cards', to='Collection.deck')),
            ],
        ),
        migrations.AddField(
            model_name='deck',
            name='deck_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_deck', to='Collection.decktype'),
        ),
    ]