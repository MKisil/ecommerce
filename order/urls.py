from django.urls import path

from .views import BuildOrderView, OrderListView, OrderDetailView

urlpatterns = [
    path('checkout/', BuildOrderView.as_view(), name='checkout'),
    path('orders/', OrderListView.as_view(), name='orders-list'),
    path('order_detail/<int:pk>/', OrderDetailView.as_view(), name='order-detail')
]