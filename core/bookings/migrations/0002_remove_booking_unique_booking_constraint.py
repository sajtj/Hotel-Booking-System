# Generated by Django 5.1 on 2025-01-21 22:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='booking',
            name='unique_booking_constraint',
        ),
    ]
