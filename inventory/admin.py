from django.contrib import admin
from .models import Category, Item, Tags

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')

class ItemAdmin(admin.ModelAdmin):
    list_display = ['sku', 'name', 'category', 'available_stock', 'in_stock']

class TagsAdmin(admin.ModelAdmin):
    list_display = ['name', 'img']

# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Tags, TagsAdmin)