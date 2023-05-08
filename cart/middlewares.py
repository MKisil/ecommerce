from .cart import Cart


class CartMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request, *args, **kwargs):
        request.cart = Cart(request.session.get('cart', {}))
        response = self._get_response(request, *args, **kwargs)
        if getattr(request, 'cart', None) is None:
            return response
        if request.cart.changed:
            request.session['cart'] = request.cart.to_dict()
            request.session.save()

        return response


class UpdateCartPrices:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request, *args, **kwargs):
        request.cart.update_prices()
        response = self._get_response(request, *args, **kwargs)
        return response
