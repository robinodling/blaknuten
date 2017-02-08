# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-22 01:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('boat_booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='end',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='start',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='booking',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='booking',
            name='submitted',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
