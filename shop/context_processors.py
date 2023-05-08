from shop.models import Category


def get_categories(request):
    return {'categories': Category.objects.prefetch_related('subcategories', 'manufacturers').all()}


def get_cart(request):
    return {'cart': request.cart}
