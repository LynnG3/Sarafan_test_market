# Generated by Django 4.2.7 on 2024-06-13 20:23

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0007_remove_shoppingcart_products_shoppingcart_product_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ShoppingCart',
            new_name='Purchase',
        ),
        migrations.AlterModelOptions(
            name='purchase',
            options={'default_related_name': 'purchase', 'verbose_name': 'Корзина покупок', 'verbose_name_plural': 'Корзины покупок'},
        ),
    ]
