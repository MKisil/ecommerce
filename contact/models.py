from django.core import validators
from django.db import models


class ShopAddress(models.Model):
    address = models.CharField(verbose_name='Адреса', max_length=300)
    city = models.CharField(verbose_name='Місто', max_length=70)
    post_code = models.CharField(verbose_name='Поштовий індекс', max_length=5, validators=[
        validators.integer_validator,
        validators.MinLengthValidator(5),
    ]
                                 )
    telephone = models.CharField(verbose_name='Телефон', max_length=11)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Адреса'
        verbose_name_plural = 'Адреси'


class Contact(models.Model):
    name = models.CharField(verbose_name='Ім\'я контакту', max_length=50)
    contact = models.CharField(verbose_name='Контакт', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакти'