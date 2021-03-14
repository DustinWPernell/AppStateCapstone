# Generated by Django 3.1.7 on 2021-02-26 17:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Snippet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200)),
                ('original_code', models.TextField()),
                ('highlighted_code', models.TextField()),
                ('exposure',
                 models.CharField(choices=[('public', 'Public'), ('unlisted', 'Unlisted'), ('private', 'Private')],
                                  max_length=10)),
                ('hits', models.IntegerField(default=0)),
                ('slug', models.SlugField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('default_exposure',
                 models.CharField(choices=[('public', 'Public'), ('unlisted', 'Unlisted'), ('private', 'Private')],
                                  default='public', max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile',
                                           to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Friends',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_one', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_one',
                                               to=settings.AUTH_USER_MODEL)),
                ('user_two', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_two',
                                               to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Followers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_one', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower_one',
                                               to=settings.AUTH_USER_MODEL)),
                ('user_two', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower_two',
                                               to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
