# Generated by Django 4.2.7 on 2024-06-10 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_remove_product_image_medium_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image_medium',
            field=models.ImageField(blank=True, null=True, upload_to='products/medium'),
        ),
        migrations.AddField(
            model_name='product',
            name='image_small',
            field=models.ImageField(blank=True, null=True, upload_to='products/small'),
        ),
    ]
