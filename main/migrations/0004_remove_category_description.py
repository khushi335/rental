# Generated by Django 5.2 on 2025-05-28 11:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_category_options_property_is_hot_deal_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='description',
        ),
    ]
