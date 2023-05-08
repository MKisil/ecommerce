from django import template

register = template.Library()


@register.filter
def add(value1, value2):
    value1, value2 = float(value1), float(value2)
    return value1 + value2


@register.filter
def multiply(value, n):
    return value * n


@register.filter
def price_with_vat(value, vat):
    value = float(value)
    return value + vat_of_price(value, vat)


@register.filter
def vat_of_price(value, vat):
    return value * vat / 100
