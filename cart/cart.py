from collections import UserDict

from django.db.models import Value, CharField
from django.db.models.functions import Concat

from order.models import OrderItem
from shop.models import ProductOptions, Product


class Cart(UserDict):
    changed = False

    def add(self, product, options_id, quantity):
        self.changed = True
        options = ProductOptions.objects.filter(id__in=options_id).values('name', 'surcharge')
        self[' '.join([product.slug]+[i['name'] for i in options])] = {
            'full_name': ' '.join([product.name]+[i['name'] for i in options]),
            'model': product.model if product.model else '---',
            'slug': product.slug,
            'id': product.id,
            'quantity': quantity,
            'max_product_quantity': product.quantity,
            'unit_price_without_options': product.get_actual_price(),
            'cost': self.product_cost(product.get_actual_price(), options, quantity)
        }

    def update_prices(self):
        self.change = True
        self.fix()
        products = Product.objects.filter(id__in=[v['id'] for v in self.values()])
        for v in self.values():
            quantity = v['quantity']
            v['cost'] = (v['cost'] - v['unit_price_without_options'] * quantity) + products.get(id=v['id']).get_actual_price() * quantity

    def change_product_quantity_and_cost(self, product, quantity):
        self.changed = True
        self[product]['cost'] = (self[product]['cost'] / self[product]['quantity']) * quantity
        self[product]['quantity'] = quantity

    def product_cost(self, price, options, quantity):
        return (sum([i['surcharge'] for i in options]) + price) * quantity

    def total_cost(self):
        return sum(i['cost'] for i in self.values())

    def build_order(self, order):
        self.fix()
        order_items = []
        for product in self.values():
            order_items.append(OrderItem(
                order=order,
                product_id=product['id'],
                full_name=product['full_name'],
                model=product['model'],
                unit_price=product['cost']/product['quantity'],
                quantity=product['quantity']
            ))
        order.items.bulk_create(order_items)

    def to_dict(self):
        return dict(self)

    def fix(self):
        '''Видаляє товари з корзини якщо їх або їхніх опцій немає в базі даних'''
        products_slug_cart = [v['slug'] for v in self.values()]
        products = Product.objects.filter(slug__in=products_slug_cart).prefetch_related('options').annotate(
            options_names=Concat('options__name', Value(' '),
                                 output_field=CharField()
                                 )).values('slug', 'options_names')

        products_dict = dict((i['slug'], i['options_names']) for i in products)

        for k, v in self.copy().items():
            if not products_dict.get(v['slug']):
                self.changed = True
                del self[k]
            elif set(k.split()[1:]) - set(products_dict[v['slug']]):
                self.changed = True
                del self[k]

    def delete(self, product):
        self.changed = True
        del self[product]

    def flush(self):
        self.changed = True
        for key in list(self):
            del self[key]



