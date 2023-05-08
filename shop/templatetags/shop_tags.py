from django import template
from django.db.models import Count

from shop.models import Manufacturer

register = template.Library()


@register.simple_tag()
def get_manufacturers():
    return Manufacturer.objects.annotate(product_count=Count('products')).filter(product_count__gt=0)

