# Generated by Django 4.2.7 on 2024-06-10 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_slug_alter_subcategory_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image_medium',
        ),
        migrations.RemoveField(
            model_name='product',
            name='image_small',
        ),
    ]