from django.db.models import Count, Sum, F
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib import messages
from django.db import transaction


from .forms import CheckoutForm, PersonalDetailsForm, AddressForm
from .models import Order
from .services import update_products_quantity


class BuildOrderView(TemplateView):
    template_name = 'order/checkout.html'

    def post(self, request, *args, **kwargs):
        personal_details_form = PersonalDetailsForm({k: v for k, v in request.POST.items() if k in PersonalDetailsForm().fields})
        address_form = AddressForm({k: v for k, v in request.POST.items() if k in AddressForm().fields})
        checkout_form = CheckoutForm(request.POST)

        if all((personal_details_form.is_valid(), address_form.is_valid(), checkout_form.is_valid())):
            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    shipping_method=checkout_form.cleaned_data['shipping_method'],
                    payment_method=checkout_form.cleaned_data['payment_method'],
                    comment=checkout_form.cleaned_data['order_comment']
                )

                personal_details = personal_details_form.save(commit=False)
                personal_details.order = order
                personal_details.save()

                address = address_form.save(commit=False)
                address.order = order
                address.save()

                request.cart.build_order(order)
                update_products_quantity({v['id']: v['quantity'] for v in request.cart.values()}, action='-')
                request.cart.flush()
            return render(request, 'order/checkout_success.html')
        else:
            messages.error(request, 'Перевірте чи погодились ви з умовами, заповнили всі поля та їх корректність')
            checkout_form.personal_details = personal_details_form
            checkout_form.address = address_form
            return self.render_to_response(self.get_context_data(form=checkout_form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if kwargs.get('form'):
            context['order_form'] = kwargs['form']
        else:
            context['order_form'] = CheckoutForm()
        return context


class OrderListView(ListView):
    model = Order
    template_name = 'order/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user_id=self.request.user).select_related('personaldetails').annotate(products=Count('items'), total_price=Sum(F('items__quantity')*F('items__unit_price')))


@method_decorator(csrf_exempt, name='dispatch')
class OrderDetailView(DetailView):
    model = Order
    template_name = 'order/order_detail.html'
    context_object_name = 'order'

    def post(self, request, *args, **kwargs):
        order_pk = request.POST['order_pk']
        order = Order.objects.get(pk=order_pk)
        order.is_active = False
        order.save()
        return HttpResponseRedirect(order.get_absolute_url())

    def get_object(self, queryset=None):
        return Order.objects.select_related(
            'personaldetails',
            'shipping_method',
            'payment_method',
            'address'
        ).prefetch_related(
            'history',
            'items'
        ).annotate(total_price=Sum(F('items__quantity')*F('items__unit_price'))).get(pk=self.kwargs[self.pk_url_kwarg])
