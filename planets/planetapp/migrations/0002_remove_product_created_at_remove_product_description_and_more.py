# Generated by Django 4.2.7 on 2025-01-10 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planetapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
        migrations.RemoveField(
            model_name='product',
            name='updated_at',
        ),
    ]
