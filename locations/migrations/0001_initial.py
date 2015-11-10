# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('is_dining_hall', models.BooleanField(default=False)),
                ('latitude', models.DecimalField(decimal_places=4, blank=True, null=True, max_digits=7)),
                ('longitude', models.DecimalField(decimal_places=4, blank=True, null=True, max_digits=7)),
                ('url', models.URLField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='OpeningHours',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('date', models.DateField(blank=True, null=True)),
                ('weekday', models.IntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')])),
                ('breakfast_from', models.TimeField(blank=True, null=True)),
                ('breakfast_to', models.TimeField(blank=True, null=True)),
                ('lunch_from', models.TimeField(blank=True, null=True)),
                ('lunch_to', models.TimeField(blank=True, null=True)),
                ('dinner_from', models.TimeField(blank=True, null=True)),
                ('dinner_to', models.TimeField(blank=True, null=True)),
                ('late_night_from', models.TimeField(blank=True, null=True)),
                ('late_night_to', models.TimeField(blank=True, null=True)),
                ('location', models.ForeignKey(to='locations.Location')),
            ],
        ),
    ]
