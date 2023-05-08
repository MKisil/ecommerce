from django.core.exceptions import ValidationError

from shop.models import Product


def phone_number_validator(value):
    if value[0] != '+' or len(value) != 13:
        raise ValidationError('Номер телефона або факсу має бути формату +(XXX)XXXXXXXXX')


def update_products_quantity(cart, action='-'):
    products = Product.objects.filter(id__in=[k for k in cart])
    for product in products:
        if action == '-':
            product.quantity -= cart[product.id]
        elif action == '+':
            product.quantity += cart[product.id]

    Product.objects.bulk_update(products, ['quantity'])


