from django.contrib import admin
from .models import Category, Product, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name','slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ('image', 'order')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'seller', 'category', 'price', 'condition', 'is_available', 'created_at')
    list_filter = ('condition', 'category', 'is_available', 'created_at')
    search_fields = ('title', 'description', 'seller__username')
    ordering = ('-created_at',)
    inlines = [ProductImageInline]

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'order', 'created_at')
    list_filter = ('created_at',)
    ordering = ('product', 'order')
