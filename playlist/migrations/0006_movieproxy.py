# Generated by Django 3.1.6 on 2021-05-04 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playlist', '0005_auto_20210504_1217'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovieProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Movie',
                'verbose_name_plural': 'Movies',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('playlist.playlist',),
        ),
    ]
