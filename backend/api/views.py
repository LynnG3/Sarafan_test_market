from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .pagination import CustomPagination
from .permissions import IsOwner
from products.models import Category, Product, Purchase, Subcategory
from .serializers import (
    CustomUserSerializer, CategorySerializer,
    ProductInCartSerializer,
    ProductSerializer,
    PurchaseSerializer,
    PurchaseGetSerializer,
    SubcategoryProductsSerializer,
)


User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = None

    def get_permissions(self):
        if self.action == "me":
            return (IsAuthenticated(),)
        return super().get_permissions()


class BaseMarketView(ListAPIView):
    """Базовый класс с общими настройками представлений. """

    pagination_class = CustomPagination
    permission_classes = [AllowAny]


class ProductListView(BaseMarketView):
    """Представление списка продуктов. """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryListView(BaseMarketView):
    """Представление категорий с подкатегориями. """

    queryset = Category.objects.prefetch_related('subcategories')
    serializer_class = CategorySerializer


class SubcategoryListView(BaseMarketView):
    """Представление категории с продуктами. """

    serializer_class = SubcategoryProductsSerializer

    def get_queryset(self):
        subcategory_slug = self.kwargs.get('subcategory_slug')
        if subcategory_slug:
            return Subcategory.objects.filter(
                slug=subcategory_slug).prefetch_related(
                    'products'
                )
        else:
            return Subcategory.objects.all().prefetch_related('products')


class PurchaseViewSet(ModelViewSet):
    """Представление для вывода состава корзины.
    с возможностью изменения количества товаров. """

    queryset = Purchase.objects.all()
    serializer_class = PurchaseGetSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        """
        Возвращает список товаров
        в корзине текущего пользователя.
        """
        user = self.request.user
        return Purchase.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        """Добавляет продукт в корзину пользователя."""
        user = request.user
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        product = get_object_or_404(Product, id=product_id)
        cart_product, created = Purchase.objects.get_or_create(
            user=user, product=product,
            defaults={'quantity': 0}
        )
    # Если объект был создан, ранее - увеличивает количество
        if not created:
            # Увеличивает количество на значение quantity из запроса
            cart_product.quantity += int(quantity)
            cart_product.save()
        else:
            # Устанавливает количество из запроса
            cart_product.quantity = int(quantity)
            cart_product.save()
        serializer = PurchaseSerializer(cart_product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        """Изменяет количество товара в корзине."""
        instance = self.get_object()
        serializer = PurchaseSerializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """ Удаляет товар из корзины. """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['delete'])
    def clear_cart(self, request, *args, **kwargs):
        """ Очищает корзину. """
        self.get_queryset().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_shoping_cart(self, request):
        """
        Возвращает состав корзины пользователя
        с общей стоимостью и данными о пользователе.
        """
        user = request.user
        cart_items = self.get_queryset()
        total_cost = sum(
            item.cost for item in cart_items
        )
        user_data = {
            'id': user.id,
            'username': user.username,
        }
        cart_data = []
        for item in cart_items:
            cart_data.append({
                'product': ProductInCartSerializer(item.product).data,
                'quantity': item.quantity,
                'cost': item.product.price * item.quantity
            })
        response_data = {
            'user': user_data,
            'total_cost': total_cost,
            'cart_items': cart_data
        }
        return Response(response_data)
