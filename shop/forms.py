from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .models import CartItem, UserProfile


class CartItemForm(forms.ModelForm):
    """Форма добавления товара"""
    class Meta:
        model = CartItem
        fields = ("quantity",)


class UserUpdateForm(forms.ModelForm):
    """Форма добавления profile"""
    # template_name = '/something/else'

    class Meta:
        model = User

        fields = (
            'email',
            'first_name',
            'last_name'
        )


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'address_type',
            'address_line',
            'address_line_2',
            'city',
            'postal_code',
            'phone',
        )
