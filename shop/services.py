import operator
import random
from collections import defaultdict

from order.models import Order
from shop.models import Category, Subcategory, Product


def get_rating_percent(rating):
    if rating:
        return round(100 * rating / 5)
    return None


def get_subcategories(url_parameters):
    cat_slug = url_parameters.get('category_slug')
    selected_manufacturer = url_parameters.get('selected_manufacturer')
    if cat_slug:
        return Category.objects.get(slug=cat_slug).subcategories.all().values('name', 'slug')
    elif selected_manufacturer:
        return Category.objects.get(slug=selected_manufacturer['category'].slug).subcategories.all().values('name', 'slug')
    else:
        subcategory = Subcategory.objects.get(slug=url_parameters['subcategory_slug'])
        return subcategory.parent_category.subcategories.all().values('name', 'slug')


def get_name_ordering(key):
    ordering_dict = {
        'name': 'Name A - Z',
        '-name': 'Name Z - A',
        'price': 'Price Low > High',
        '-price': 'Price High > Low',
        'average-rating': 'Rating Highest',
        '-average_rating': 'Rating Lowest',
        'model': 'Model A - Z',
        '-model': 'Model Z - A'
    }

    if key:
        return ordering_dict.get(key)


def get_bestsellers():
    total_number_of_purchases = defaultdict(int)
    orders = Order.objects.filter(received=True).prefetch_related('items')
    for order in orders:
        for item in order.items.all().select_related('product'):
            total_number_of_purchases[item.product] += item.quantity

    return total_number_of_purchases if len(total_number_of_purchases) < 11 else dict(sorted(total_number_of_purchases.items(), key=operator.itemgetter(1), reverse=True)[:11])


def get_featured(request, is_authenticated=False):
    if request.cart or is_authenticated:
        products = []
        if request.cart:
            product = Product.objects.get(pk=random.choice([v['id'] for v in request.cart.values()]))
            products = product.category.products.all()

        if is_authenticated and not request.cart:
            if request.user.orders.exists():
                product = random.choice(random.choice(request.user.orders.all().prefetch_related('items')).items.all().select_related('product')).product
                products = product.category.products.all()

        return products if len(products) <= 5 else [random.choice(products) for _ in range(5)]


def get_related_products(product):
    category = Subcategory.objects.prefetch_related('products').get(pk=product.category_id)
    products = category.products.all()
    return products if products.count() <= 5 else [random.choice(products) for _ in range(5)]


def get_latest_products():
    products = Product.objects.all()
    return products if len(products) <= 6 else products[6:]


def get_special_products():
    products = Product.objects.filter(discount__gt=0)
    return products if len(products) <= 6 else products[6:]





