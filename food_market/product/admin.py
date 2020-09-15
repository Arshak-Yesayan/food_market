from django.contrib import admin

from product.models import Product, Category, Subcategory, Like

# Register your models here.

# class ProductAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug':('title',)}

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Like)