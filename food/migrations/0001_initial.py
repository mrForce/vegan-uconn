# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=1000, blank=True)),
                ('category', models.CharField(max_length=100)),
                ('is_vegan', models.BooleanField(default=False)),
                ('is_gluten_free', models.BooleanField(default=False)),
                ('contains_nuts', models.BooleanField(default=False)),
                ('date', models.DateField()),
                ('meal', models.CharField(max_length=2, choices=[('Br', 'Breakfast'), ('Lu', 'Lunch'), ('Di', 'Dinner'), ('LN', 'Late Night'), ('LD', 'Lunch & Dinner'), ('TM', "Today's Menu"), ('No', 'None!')], default='Br')),
                ('price', models.CharField(max_length=20, null=True, blank=True)),
                ('location', models.ForeignKey(to='locations.Location')),
            ],
        ),
    ]
