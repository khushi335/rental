# Generated by Django 5.2 on 2025-06-19 09:17

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_rename_created_at_findmeroom_date_requested_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='findmeroom',
            old_name='date_requested',
            new_name='submitted_at',
        ),
        migrations.RemoveField(
            model_name='findmeroom',
            name='category',
        ),
        migrations.RemoveField(
            model_name='findmeroom',
            name='location',
        ),
        migrations.RemoveField(
            model_name='findmeroom',
            name='user',
        ),
        migrations.AddField(
            model_name='findmeroom',
            name='email',
            field=models.EmailField(default=django.utils.timezone.now, max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='findmeroom',
            name='full_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='findmeroom',
            name='phone',
            field=models.CharField(default=django.utils.timezone.now, max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='findmeroom',
            name='preferred_location',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='findmeroom',
            name='room_type',
            field=models.CharField(choices=[('single', 'Single Room'), ('shared', 'Shared Room'), ('flat', 'Flat/Apartment'), ('hostel', 'Hostel')], default=django.utils.timezone.now, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='findmeroom',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
    ]
