from django.contrib import admin
from django import forms

from mptt.admin import MPTTModelAdmin

from photologue.admin import GalleryAdmin as GalleryAdminDefault
from photologue.models import Gallery

from .models import (Category, Product, Cart, CartItem, Order, UserProfile)


class CategoryMPTTModelAdmin(MPTTModelAdmin):
    mptt_level_indent = 20


class ProductAdmin(admin.ModelAdmin):
    """Продукты"""
    list_display = ("title", "category", "price", "quantity")
    prepopulated_fields = {"slug": ("title",)}


class CartItemAdmin(admin.ModelAdmin):
    """Товары в корзине"""
    list_display = ("cart", "product", "quantity")


class GalleryAdminForm(forms.ModelForm):
    """Users never need to enter a description on a gallery."""

    class Meta:
        model = Gallery
        exclude = ['description']


class GalleryAdmin(GalleryAdminDefault):
    form = GalleryAdminForm


admin.site.unregister(Gallery)
admin.site.register(Gallery, GalleryAdmin)

admin.site.register(Category, CategoryMPTTModelAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order)
admin.site.register(UserProfile)
