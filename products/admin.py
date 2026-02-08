from django.contrib import admin
from .models import Category, Product
# Register your models here.
@admin.register(Category)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name','slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'seller', 'category', 'price', 'condition', 'is_available', 'created_at')
    list_filter = ('condition', 'category', 'is_available', 'created_at')
    search_fields = ('title', 'description', 'seller__username')
    ordering = ('-created_at',)
