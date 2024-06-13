import io

from PIL import Image
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer, UserSerializer

from market_backend.constants import (
    IMAGE_SMALL_SIZE, IMAGE_MEDIUM_SIZE, IMAGE_LARGE_SIZE
)
from products.models import Category, Product, Purchase, Subcategory


User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериализатор для кастомной модели пользователя."""


class Meta:
    model = User
    fields = (
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
    )


class CreateCustomUserSerializer(UserCreateSerializer):
    """Сериализатор для создания кастомной модели пользователя."""

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ("key",)


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор списка продуктов. """

    image_large = serializers.ImageField(required=True)
    image_medium = serializers.SerializerMethodField()
    image_small = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'slug',
            'price',
            'category',
            'subcategory',
            'image_small',
            'image_medium',
            'image_large'
        )

    def create(self, validated_data):
        image_large = validated_data.pop('image_large')
        product = Product.objects.create(**validated_data)
        # Проверяет размер изначально загруженного изображения
        if (
            image_large.width == IMAGE_LARGE_SIZE[0]
            and image_large.height == IMAGE_LARGE_SIZE[1]
        ):
            image_large = image_large
        else:
            # Изменяет размер загруженного изображения,
            # если оно не соответствует заданному
            image_large = self.resize_image(image_large, IMAGE_LARGE_SIZE)
        # Сохранет исходное изображение в нужном размере
        product.image_large.save(
            f"{product.slug}_large.jpg", image_large, save=True
        )
        # Сохраняет изображения в среднем и маленьком размерах
        self.get_image_medium(product)
        self.get_image_small(product)
        product.save()
        return product

    def get_image_medium(self, obj):
        if not obj.image_medium:
            image_medium = self.resize_image(
                obj.image_large, IMAGE_MEDIUM_SIZE
            )
            obj.image_medium.save(
                f"{obj.slug}_medium.jpg",
                image_medium, save=True
            )
        return obj.image_medium.url

    def get_image_small(self, obj):
        if not obj.image_small:
            image_small = self.resize_image(
                obj.image_large, IMAGE_SMALL_SIZE
            )
            obj.image_small.save(
                f"{obj.slug}_small.jpg",
                image_small, save=True
            )
        return obj.image_small.url

    def resize_image(self, image, size):
        """
        Изменяет размер загруженного изображения
        в соответсвии с требованиями, заданными в backend/constants.py
        """
        image.seek(0)
        img = Image.open(image)
        img.thumbnail(size, resample=Image.BICUBIC)

        new_image = io.BytesIO()
        img.save(new_image, format='JPEG')
        return ContentFile(new_image.getvalue())


class SubcategorySerializer(serializers.ModelSerializer):
    """Сериализатор подкатегорий. """

    class Meta:
        model = Subcategory
        fields = (
            'id',
            'name',
            'slug',
            'image'
        )


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор списка категорий c подкатегориями. """

    subcategories = SubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'slug',
            'image',
            'subcategories'
        )


class SubcategoryProductsSerializer(serializers.ModelSerializer):
    """Сериализатор подкатегории с продуктами. """

    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Subcategory
        fields = (
            'id',
            'name',
            'slug',
            'image',
            'products'
        )


class ProductInCartSerializer(serializers.ModelSerializer):
    """Сериализатор продукта для корзины. """

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'price',
            'image_small',
        )

    def get_image_small(self, obj):
        return obj.image_small


class PurchaseSerializer(serializers.ModelSerializer):
    """Сериализатор создания покупки
    для добавления товара в корзину."""

    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
    )

    class Meta:
        model = Purchase
        fields = ('user', 'product_id', 'quantity', 'cost')


class PurchaseGetSerializer(serializers.ModelSerializer):
    """Сериализатор представления товара в корзине."""

    product = ProductInCartSerializer(read_only=True)

    class Meta:
        model = Purchase
        fields = ('product', 'quantity', 'cost')
