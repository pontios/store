from django.urls import path

from . import views


urlpatterns = [
    path("", views.ProductsList.as_view(), name="product_all"),
    path('detail/<slug:slug>/', views.ProductDetail.as_view(), name='product_detail'),
    path("add-cart-item/<slug:slug>/<int:pk>/", views.AddCartItem.as_view(), name="add_cartitem"),
    path("cart/", views.CartItemList.as_view(), name="cart_item"),
    path("delete/<int:pk>/", views.RemoveCartItem.as_view(), name="del_item"),
    path("edit/<int:pk>/", views.EditCartItem.as_view(), name="edit_item"),
    path("search/", views.Search.as_view(), name="search"),
    path("add-order/", views.AddOrder.as_view(), name="add_order"),
    path("orders/", views.OrderList.as_view(), name="orders"),
    path("category/<slug:slug>/", views.CategoryProduct.as_view(), name="category"),
    path('profile/', views.UserProfile.as_view(), name='user_profile'),
    path('profile/edit/', views.EditProfile.as_view(), name='edit_profile'),
    path('checkout/', views.Checkout.as_view(), name='checkout'),
    path('order-complete/', views.OrderComplete.as_view(), name='order_complete'),
]