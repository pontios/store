from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .models import CartItem, UserProfile


class CartItemForm(forms.ModelForm):
    """Форма добавления товара"""
    class Meta:
        model = CartItem
        fields = ("quantity",)



