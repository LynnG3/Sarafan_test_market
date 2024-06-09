from django.contrib import admin
from .models import Category, Subcategory, Product


class SubcategoryInline(admin.StackedInline):
    model = Subcategory
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Панель администрирования категорий."""

    inlines = [SubcategoryInline]
    list_display = (
        'id',
        'name',
        'slug',
        'image'
    )
    readonly_fields = ('id',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    """Панель администрирования подкатегорий."""

    list_display = (
        'id',
        'name',
        'slug',
        'category',
        'image'
    )
    readonly_fields = ('id',)
    search_fields = ('name', 'slug', 'category__name',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('category',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            kwargs["queryset"] = Category.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Панель администрирования продуктов."""

    list_display = (
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
    readonly_fields = ('id',)
    search_fields = ('name', 'slug', 'category__name', 'subcategory__name')
    prepopulated_fields = {'slug': ('name',)}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'subcategory':
            if 'category' in request.GET:
                category_id = int(request.GET['category'])
                kwargs["queryset"] = Subcategory.objects.filter(
                    category_id=category_id
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
