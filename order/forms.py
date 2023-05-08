from django import forms

from .models import ShippingMethod, PaymentMethod, PersonalDetails, Address, Order


class PersonalDetailsForm(forms.ModelForm):

    class Meta:
        model = PersonalDetails
        fields = ('first_name', 'last_name', 'email', 'telephone', 'fax')
        widgets = {field_name: forms.TextInput(attrs={'size': 30}) for field_name in PersonalDetails._meta.get_fields()}


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ('company', 'address1', 'address2', 'city', 'post_code')
        widgets = {field_name: forms.TextInput(attrs={'size': 30}) for field_name in Address._meta.get_fields()}


class CheckoutForm(forms.Form):
    personal_details = PersonalDetailsForm()
    address = AddressForm()
    delivery_billing_address = forms.BooleanField(label='Мої адреси доставки та виставлення рахунку однакові.', required=True)
    shipping_method = forms.ModelChoiceField(label='Спосіб доставки', queryset=ShippingMethod.objects.all(), widget=forms.RadioSelect, required=True)
    payment_method = forms.ModelChoiceField(label='Спосіб оплати', queryset=PaymentMethod.objects.all(), widget=forms.RadioSelect, required=True)
    order_comment = forms.CharField(label='Коментар', widget=forms.Textarea(attrs={'rows': 8, 'style': 'width: 99%;'}))
    terms_and_conditions_accepted = forms.BooleanField(label='Я прочитав і погоджуюся з умовами', required=True)


