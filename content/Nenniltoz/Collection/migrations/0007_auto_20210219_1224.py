# Generated by Django 3.1.6 on 2021-02-19 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Collection', '0006_auto_20210218_1224'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='id',
        ),
        migrations.AlterField(
            model_name='card',
            name='cardID',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='cardface',
            name='cardID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Collection.card'),
        ),
        migrations.AlterField(
            model_name='legality',
            name='cardID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Collection.card'),
        ),
    ]