from django.core.exceptions import FieldError, ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import *
from django.views.generic.edit import FormMixin
from django_registration import signals
from django_registration.backends.activation.views import RegistrationView

from cart.forms import AddToCartForm
from .models import *
from .forms import *
from .services import (
    get_rating_percent,
    get_subcategories,
    get_name_ordering,
    get_bestsellers,
    get_featured,
    get_related_products,
    get_special_products,
    get_latest_products
)


class HomeView(TemplateView):
    template_name = 'shop/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_products'] = get_latest_products()
        context['special_products'] = get_special_products()
        context['banners'] = Banner.objects.filter(draft=False)
        return context


class ProductDetailView(FormMixin, DetailView):
    model = Product
    form_class = ReviewForm

    def post(self, request, *args, **kwargs):

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            self.object = self.get_object()
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('shop:product-detail', kwargs={'slug': self.kwargs['slug']})

    def form_valid(self, form):
        product = self.get_object()

        review = form.save(commit=False)
        review.product = product
        review.save()

        product.average_rating = (product.evaluated_cnt * product.average_rating + review.rating) / (product.evaluated_cnt + 1)
        product.evaluated_cnt += 1
        product.save()

        return super().form_valid(form)

    def paginate_reviews(self, number):
        paginator = Paginator(self.object.reviews.all(), number)

        try:
            page_number = paginator.validate_number(self.request.GET.get('page', 1))
        except PageNotAnInteger:
            page_number = 1
        except EmptyPage:
            page_number = paginator.num_pages

        return paginator.page(page_number)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        context['page_reviews'] = self.paginate_reviews(5)
        context['rating'] = get_rating_percent(context['object'].average_rating)
        if self.request.GET.get('cart_form', None):
            context['cart_form'] = self.request.GET.get('cart_form')
        else:
            context['cart_form'] = AddToCartForm(product=product)
        context['photos'] = context['object'].photos.all()
        context['bestsellers'] = get_bestsellers()
        context['featured'] = get_featured(self.request, self.request.user.is_authenticated)
        context['related_products'] = get_related_products(context['object'])

        return context


class ListProductCategoryView(ListView):
    template_name = 'shop/list_product_category.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        subcategory_slug = self.kwargs.get('subcategory_slug')
        if subcategory_slug:
            queryset = get_object_or_404(Subcategory, slug=subcategory_slug).products.filter(selling=True)
        else:
            subcategories = get_object_or_404(Category, slug=self.kwargs['category_slug']).subcategories.all().values('name')
            queryset = Product.objects.filter(Q(category__name__in=subcategories) & Q(selling=True))

        try:
            return queryset.order_by(self.request.GET['ordering']) if self.request.GET.get('ordering') else queryset
        except (FieldError, KeyError):
            return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subcategories'] = get_subcategories(self.kwargs)
        context['ordering_name'] = get_name_ordering(self.request.GET.get('ordering'))
        context['bestsellers'] = get_bestsellers()
        context['featured'] = get_featured(self.request, self.request.user.is_authenticated)

        return context


class ListProductManufacturerView(ListProductCategoryView):
    def get_queryset(self):
        manufacturer = get_object_or_404(Manufacturer, slug=self.kwargs['manufacturer_slug'])

        self.kwargs.update({'subcategory_slug': self.request.GET.get('subcategory_slug'),
                            'category_slug': self.request.GET.get('category_slug'),
                            'selected_manufacturer': {'name': manufacturer.name, 'category': manufacturer.category}
                            })

        if self.request.GET.get('subcategory'):
            return manufacturer.products.filter(
                Q(category__slug=self.request.GET['subcategory']) & Q(selling=True)
            )
        if self.request.GET.get('category'):
            return manufacturer.products.filter(
                Q(category__parent_category__slug=self.request.GET['category']) & Q(selling=True)
            )

        return manufacturer.products.filter(selling=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_manufacturer'] = self.kwargs['selected_manufacturer']['name']
        return context


class SendActivationEmailAgainView(RegistrationView):
    form_class = EmailForm
    template_name = "django_registration/activation_failed.html"

    def get(self, request, *args, **kwargs):
        return HttpResponseNotFound()

    def register(self, form):
        user = self.get_inactive_user(form)
        signals.user_registered.send(
            sender=self.__class__, user=user, request=self.request
        )
        return user

    def get_inactive_user(self, form):
        if form.is_valid():
            user = form.cleaned_data['user']
            self.send_activation_email(user)
            return user
        return render(self.request, 'django_registration/activation_failed.html', {'form': form})

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        return form_class(**self.get_form_kwargs())