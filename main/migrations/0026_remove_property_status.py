# Generated by Django 5.2 on 2025-06-21 08:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_property_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='status',
        ),
    ]
