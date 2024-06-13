from django.db import models
from django.utils.text import slugify

from users.models import CustomUser


class Category(models.Model):
    """Модель категории продукта. """

    name = models.CharField(
        max_length=100
    )
    slug = models.SlugField(
        unique=True
    )
    image = models.ImageField(
        upload_to='subcategories'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    """Модель подкатегории продукта. """

    name = models.CharField(
        max_length=100
    )
    slug = models.SlugField(
        unique=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to='subcategories'
    )

    class Meta:
        ordering = ('name',)
        default_related_name = 'subcategories'
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель продукта. """

    name = models.CharField(
        max_length=200
    )
    slug = models.SlugField(
        unique=True
    )
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    price = models.DecimalField(
        max_digits=8, decimal_places=2
    )
    image_small = models.ImageField(
        upload_to='products/small',
        null=True,
        blank=True
    )
    image_medium = models.ImageField(
        upload_to='products/medium',
        null=True,
        blank=True
    )
    image_large = models.ImageField(
        upload_to='products/large'
    )

    class Meta:
        ordering = ('name',)
        default_related_name = 'products'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Purchase(models.Model):
    """Модель покупки в корзине. """

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    product = models.ForeignKey(
        Product,
        null=True,
        default=None,
        on_delete=models.CASCADE,
        verbose_name='Продукты'
    )
    quantity = models.PositiveSmallIntegerField(
        null=True,
        default=None,
        verbose_name='Количество'
    )

    class Meta:
        default_related_name = 'purchase'
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзины покупок'

    @property
    def cost(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'Корзина пользователя {self.user.username}'
