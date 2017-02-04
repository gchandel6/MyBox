# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-12 06:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ep_name', models.CharField(blank=True, max_length=50, null=True)),
                ('number', models.IntegerField()),
                ('first_aired', models.DateField(null=True)),
                ('date_watched', models.DateField(auto_now=True, null=True)),
                ('status_watched', models.BooleanField(default=False)),
                ('overview', models.TextField(blank=True, null=True)),
                ('tvdb_id', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('status_watched', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tvdbID', models.CharField(max_length=50)),
                ('series_name', models.CharField(max_length=50)),
                ('overview', models.TextField()),
                ('banner', models.CharField(blank=True, max_length=140, null=True)),
                ('imbdID', models.CharField(blank=True, max_length=50, null=True)),
                ('status_watched', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('running_status', models.CharField(max_length=100)),
                ('first_aired', models.DateField(null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('siteRating', models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=5, null=True)),
                ('userRating', models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=5, null=True)),
                ('network', models.CharField(max_length=50)),
                ('genre_list', models.TextField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='season',
            name='show',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myshows.Show'),
        ),
        migrations.AddField(
            model_name='episode',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myshows.Season'),
        ),
    ]