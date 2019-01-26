from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.views.generic.base import View

from store import settings
from .models import (Product, Cart, CartItem, Order, Category)
from .forms import CartItemForm, UserUpdateForm, ProfileUpdateForm


class ProductsList(ListView):
    """Список всех продуктов"""
    model = Product
    template_name = "shop/list-product.html"


class ProductDetail(DetailView):
    """Карточка товара"""
    model = Product
    context_object_name = 'product'
    template_name = 'shop/product-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CartItemForm()
        return context


class AddCartItem(View):
    """Добавление товара в карзину"""
    def post(self, request, slug, pk):
        quantity = request.POST.get("quantity", None)
        if quantity is not None and int(quantity) > 0:
            try:
                item = CartItem.objects.get(cart__user=request.user, cart__accepted=False, product_id=pk)
                item.quantity += int(quantity)
            except CartItem.DoesNotExist:
                item = CartItem(
                    cart=Cart.objects.get(user=request.user, accepted=False),
                    product_id=pk,
                    quantity=int(quantity)
                )
            item.save()
            messages.add_message(request, settings.MY_INFO, "Товар добавлен")
            return redirect("/detail/{}/".format(slug))
        else:
            messages.add_message(request, settings.MY_INFO, "Значение не может быть 0")
            return redirect("/detail/{}/".format(slug))


class CartItemList(ListView):
    """Товары в корзине подьзователя"""
    template_name = 'shop/cart.html'

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user, cart__accepted=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart_id"] = Cart.objects.get(user=self.request.user, accepted=False).id
        return context


class EditCartItem(View):
    """Редактирование товара в карзине"""
    def post(self, request, pk):
        quantity = request.POST.get("quantity", None)
        if quantity:
            item = CartItem.objects.get(id=pk, cart__user=request.user)
            item.quantity = int(quantity)
            item.save()
        return redirect("cart_item")


class RemoveCartItem(View):
    """Удаление товара из корзины"""
    def get(self, request, pk):
        CartItem.objects.get(id=pk, cart__user=request.user).delete()
        messages.add_message(request, settings.MY_INFO, 'Товар удален')
        return redirect("cart_item")


class Search(View):
    """Поиск товаров"""
    def get(self, request):
        search = request.GET.get("search", None)
        products = Product.objects.filter(Q(title__icontains=search) |
                                          Q(category__name__icontains=search))
        return render(request, "shop/list-product.html", {"object_list": products})


class AddOrder(View):
    """Создание заказа"""
    def post(self, request):
        cart = Cart.objects.get(id=request.POST.get("pk"), user=request.user)
        cart.accepted = True
        cart.save()
        Order.objects.create(cart=cart)
        Cart.objects.create(user=request.user)
        return redirect('order_complete')


class OrderList(ListView):
    """Список заказов пользователя"""
    template_name = "shop/order-list.html"

    def get_queryset(self):
        return Order.objects.filter(cart__user=self.request.user, accepted=False)

    def post(self, request):
        order = Order.objects.get(id=request.POST.get("pk"), cart__user=request.user, accepted=False)
        order.delete()
        return redirect("orders")


class CategoryProduct(ListView):
    """Список товаров из категории"""
    template_name = "shop/list-product.html"

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        node = Category.objects.get(slug=slug)
        if Product.objects.filter(category__slug=slug).exists():
            products = Product.objects.filter(category__slug=slug)
        else:
            products = Product.objects.filter(category__slug__in=[x.slug for x in node.get_family()])
        return products


class UserProfile(View):
    """profile view"""

    def get(self, request, pk=None):
        if pk:
            user = User.objects.get(pk=pk)
        else:
            user = request.user
        context = {
            'user': user
        }
        return render(request, 'shop/profile.html', context)


class EditProfile(UpdateView):
    """edit profile"""

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        u_form = ProfileUpdateForm(instance=request.user.userprofile)
        forms = {
            'form': form,
            'u_form': u_form
        }
        return render(request, 'shop/edit-profile.html', forms)

    def post(self, request):
        if request.method == 'POST':
            form = UserUpdateForm(request.POST, instance=request.user)
            u_form = ProfileUpdateForm(request.POST, instance=request.user.userprofile)

            if form.is_valid() and u_form.is_valid():
                form.save()
                u_form.save()
                return redirect('user_profile')


class Checkout(View):
    """ checkout"""

    def get(self, request, total=0):
        cart_item = CartItem.objects.filter(cart__user=self.request.user, cart__accepted=False)
        for item in cart_item:
            total += (item.product.price * item.quantity)
        form = UserUpdateForm(instance=request.user)
        u_form = ProfileUpdateForm(instance=request.user.userprofile)
        cart_id = Cart.objects.get(user=self.request.user, accepted=False).id
        context = {
            'form': form,
            'u_form': u_form,
            'cart_item': cart_item,
            'total': total,
            'cart_id': cart_id
        }
        return render(request, 'shop/checkout.html', context)


class OrderComplete(View):

    def get(self, request):
        user = request.user
        name = user.first_name
        context = {'name': name}
        return render(request, 'shop/order-complete.html', context)
    # def get(self, request):
    #
    #     try:
    #         cart = Cart.objects.get(user=request.user, accepted=False)
    #         cart_item = CartItem.objects.filter(cart=cart)
    #     except cart_item.DoesNotExist:
    #         return redirect('/')
    #     new_order, created = Order.objects.get_or_create(cart=cart)
    #     if created:
    #         cart = Cart.objects.get(user=request.user, accepted=False)
    #         cart.accepted = True
    #         cart.save()
    #         new_order.cart = cart
    #         new_order.save()
    #         Cart.objects.create(user=request.user)
    #     return redirect('/')



