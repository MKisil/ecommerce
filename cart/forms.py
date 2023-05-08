from django import forms

from .services import get_product_parameters


class AddToCartForm(forms.Form):
    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product')
        self.product = product
        super().__init__(*args, **kwargs)
        for parameter, options in get_product_parameters(product).items():
            self.fields[parameter.name] = forms.ChoiceField(label=parameter.name, choices=options)

    quantity = forms.IntegerField(label='Qty', widget=forms.TextInput(attrs={'size': 2}))

