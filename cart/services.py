from django.contrib import messages

from shop.models import Product


def get_product_parameters(product):
    parameters = {}
    for option in product.options.all().select_related('parameter'):
        parameters.setdefault(option.parameter, []).append(
            (option.pk, f'{option.name} {f"+{option.surcharge} eur" if option.surcharge else ""}')
        )
    return parameters


def get_products_in_cart(cart):
    cart.fix()
    products_in_cart = {product.slug: product for product in Product.objects.filter(slug__in=[v['slug'] for v in cart.values()])}
    products = {}
    for k, v in cart.items():
        products[k] = {
            'full_name': v['full_name'],
            'slug': v['slug'],
            'image': products_in_cart[v['slug']].photo.url,
            'model': v['model'],
            'quantity': v['quantity'],
            'unit_price': v['cost'] / v['quantity'],
            'total_price': v['cost']
        }

    return products


def update_user_cart(request, new_values, cart):
    for k, v in new_values.items():
        if k[0:6] == 'remove':
            cart.delete(v)
        if k[0:8] == 'quantity':
            if k[9:] in cart and v:
                try:
                    v = int(v)
                    print(v)
                    if int(v) > cart[k[9:]]['max_product_quantity']:
                        messages.error(request, f'Помилка: товару {k[9:]} такої кількості не достатньо на складі')
                        continue
                except ValueError:
                    messages.error(request, f'Помилка: ви ввели не число для продукту -- {k[9:]}')
                else:
                    request.cart.change_product_quantity_and_cost(k[9:], int(v))


def remove_product_from_cart(request):
    request.cart.delete(request.POST.get('product'))


def check_quantity_and_add(request, product, info_dict):
    quantity = int(info_dict.pop('quantity'))
    if product.quantity - quantity < 0 or quantity <= 0:
        messages.error(request, 'Помилка: товару такої кількості не достатньо на складі або ви ввели не дійсне число')
        return

    options = [int(i) for i in info_dict.values()]
    request.cart.add(product, options, quantity)
    messages.success(request, 'Товар успішно додано у корзину')





