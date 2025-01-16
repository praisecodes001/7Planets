# Generated by Django 4.2.7 on 2025-01-10 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planetapp', '0002_remove_product_created_at_remove_product_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image_url',
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(null=True, upload_to='products/'),
        ),
    ]
