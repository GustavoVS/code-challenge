# Generated by Django 2.1.7 on 2019-03-19 06:05

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pdv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trading_name', models.CharField(max_length=255, verbose_name='Trading Name')),
                ('owner_name', models.CharField(max_length=100, verbose_name='Owner Name')),
                ('document', models.CharField(max_length=34, unique=True, verbose_name='Document')),
                ('coverage_area', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('address', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
            options={
                'verbose_name': 'PDV',
                'verbose_name_plural': 'PDVs',
            },
        ),
    ]

