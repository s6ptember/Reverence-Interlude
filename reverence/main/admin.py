from django.contrib import admin
from .models import Size, Category, \
    ClothingItem, ClothingItemSize, ItemImage


class ClothingItemSizeInline(admin.TabularInline):
    model = ClothingItemSize
    extra = 4


class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 4


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(ClothingItem)
class ClothingItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category',
                    'available', 'price', 'discount',
                    'created_at', 'updated_at')
    list_filter = ('available', 'category')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('-created_at',)
    inlines = [ClothingItemSizeInline, ItemImageInline]
