# Generated by Django 3.1.7 on 2021-03-13 00:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Users', '0007_userprofile_avatarimg'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='default_exposure',
            new_name='cardView',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='deckView',
            field=models.CharField(choices=[('public', 'Public'), ('unlisted', 'Unlisted'), ('private', 'Private')],
                                   default='public', max_length=10),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='profileView',
            field=models.CharField(choices=[('public', 'Public'), ('unlisted', 'Unlisted'), ('private', 'Private')],
                                   default='public', max_length=10),
        ),
        migrations.CreateModel(
            name='UserCards',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cardID', models.CharField(max_length=200)),
                ('quantity', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_card',
                                           to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
