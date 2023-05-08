from django.urls import path
from .views import ProductDetailView, HomeView, ListProductCategoryView, ListProductManufacturerView

app_name = 'shop'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product_detail/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('category/<slug:category_slug>/', ListProductCategoryView.as_view(), name='products-category'),
    path('subcategory/<slug:subcategory_slug>/', ListProductCategoryView.as_view(), name='products-subcategory'),
    path('manufacturer/<slug:manufacturer_slug>/', ListProductManufacturerView.as_view(), name='products-manufacturer')
]
