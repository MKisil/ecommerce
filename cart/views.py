from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.generic import TemplateView

from shop.models import Product
from .forms import AddToCartForm
from .services import get_products_in_cart, update_user_cart, check_quantity_and_add, remove_product_from_cart


@method_decorator(csrf_exempt, name='dispatch')
class CartUpdateView(View):
    def post(self, request, *args, **kwargs):
        redirect_url = HttpResponseRedirect(reverse('shop:product-detail', kwargs={'slug': kwargs['product_slug']}))

        if request.POST.get('remove'):
            remove_product_from_cart(request)
            return redirect_url

        product = get_object_or_404(Product, slug=self.kwargs['product_slug'])
        mutable_query_dict = request.POST.copy().dict()
        form = AddToCartForm(mutable_query_dict, product=product)

        if not form.is_valid():
            messages.error(request, 'Помилка: ви ввели не число')
            return redirect_url

        check_quantity_and_add(request, product, mutable_query_dict)
        return redirect_url


@method_decorator(csrf_protect, name='dispatch')
class CartView(TemplateView):
    template_name = 'cart/cart.html'

    def post(self, request, *args, **kwargs):
        update_user_cart(request, request.POST, request.cart)
        return redirect(request.META.get('HTTP_REFERER'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = get_products_in_cart(self.request.cart)
        return context
