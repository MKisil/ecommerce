from django.urls import path

from cart.views import CartUpdateView, CartView

urlpatterns = [
    path('update/<slug:product_slug>/', CartUpdateView.as_view(), name='cart-update'),
    path('view/', CartView.as_view(), name='cart-view'),
]