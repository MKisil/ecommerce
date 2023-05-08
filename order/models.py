from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models
from django.urls import reverse_lazy

from shop.models import Product
from .services import phone_number_validator

User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(User, verbose_name='Користувач', null=True, blank=True, on_delete=models.SET_NULL, related_name='orders')
    shipping_method = models.ForeignKey('ShippingMethod', verbose_name='Спосіб доставки', on_delete=models.PROTECT, related_name='orders')
    payment_method = models.ForeignKey('PaymentMethod', verbose_name='Спосіб оплати', on_delete=models.PROTECT, related_name='orders')
    comment = models.TextField(verbose_name='Коментар до замовлення', blank=True)
    sent = models.BooleanField(verbose_name='Відправлено', default=False)
    received = models.BooleanField(verbose_name='Отримано', default=False)
    is_active = models.BooleanField(verbose_name='Активне', default=True)
    date_create = models.DateField(auto_now_add=True, verbose_name='Дата замовлення')

    def get_absolute_url(self):
        return reverse_lazy('order-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'Замовлення id - {self.pk}'

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'


class PersonalDetails(models.Model):
    order = models.OneToOneField('Order', verbose_name='Замовлення', on_delete=models.CASCADE)
    first_name = models.CharField(verbose_name='Ім\'я', max_length=150)
    last_name = models.CharField(verbose_name='Прізвище', max_length=150)
    email = models.EmailField(verbose_name='E-mail', max_length=150)
    telephone = models.CharField(verbose_name='Телефон', max_length=13, validators=[phone_number_validator])
    fax = models.CharField(verbose_name='Факс', max_length=13, blank=True, validators=[phone_number_validator])


class Address(models.Model):
    order = models.OneToOneField('Order', verbose_name='Замовлення', on_delete=models.CASCADE)
    company = models.CharField(verbose_name='Компанія', max_length=200, blank=True)
    address1 = models.CharField(verbose_name='Адреса', max_length=300)
    address2 = models.CharField(verbose_name='Деталі адреси', max_length=100, blank=True)
    city = models.CharField(verbose_name='Місто', max_length=100)
    post_code = models.CharField(verbose_name='Поштовий індекс', max_length=5, validators=[validators.MinLengthValidator(5)])


class ShippingMethod(models.Model):
    name = models.CharField('Метод доставки', max_length=150)
    cost = models.DecimalField(verbose_name='Вартість', max_digits=4, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Метод доставки'
        verbose_name_plural = 'Методи доставки'


class PaymentMethod(models.Model):
    name = models.CharField('Метод оплати', max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Метод оплати'
        verbose_name_plural = 'Методи оплати'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='Замовлення', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.PROTECT, related_name='items')
    full_name = models.CharField(verbose_name='Повна назва', max_length=350)
    model = models.CharField(verbose_name='Модель', max_length=150)
    unit_price = models.DecimalField(verbose_name='Ціна', max_digits=20, decimal_places=2)
    quantity = models.PositiveIntegerField(verbose_name='Кількість', default=1)


class OrderHistory(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='history')
    status = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

