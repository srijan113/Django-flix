# Generated by Django 3.1.6 on 2021-05-03 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('playlist', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playlist',
            name='live',
        ),
        migrations.AddField(
            model_name='playlist',
            name='order',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='playlist',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='playlist.playlist'),
        ),
    ]
