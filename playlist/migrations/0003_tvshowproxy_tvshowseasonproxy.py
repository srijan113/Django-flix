# Generated by Django 3.1.6 on 2021-05-03 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playlist', '0002_auto_20210503_1535'),
    ]

    operations = [
        migrations.CreateModel(
            name='TVShowProxy',
            fields=[
            ],
            options={
                'verbose_name': 'TV Show',
                'verbose_name_plural': 'TV Shows',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('playlist.playlist',),
        ),
        migrations.CreateModel(
            name='TVShowSeasonProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Season',
                'verbose_name_plural': 'Season',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('playlist.playlist',),
        ),
    ]