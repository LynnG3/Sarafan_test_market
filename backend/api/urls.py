from django.urls import include, path
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .views import (
    CategoryListView,
    ProductViewSet, SubcategoryListView,
    PurchaseViewSet, CustomUserViewSet,
)

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register(
    r'purchase', PurchaseViewSet, basename='purchase'
)
router.register(r'users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('', include("djoser.urls")),
    path('', include("djoser.urls.authtoken")),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path(
        'subcategories/<slug:subcategory_slug>/',
        SubcategoryListView.as_view(),
        name='subcategory-detail'
    ),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
]
