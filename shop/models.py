from autoslug import AutoSlugField
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(
        _('email address'),
        unique=True,
    )


class Product(models.Model):
    name = models.CharField(verbose_name='Назва', max_length=150)
    price = models.FloatField(verbose_name='Ціна', validators=[validators.MinValueValidator(0.01)])
    model = models.CharField(verbose_name='Модель', max_length=150, blank=True)
    quantity = models.IntegerField(verbose_name='Кількість на складі', default=0, null=True, validators=[validators.MinValueValidator(0)])
    manufacturer = models.ForeignKey(
        'Manufacturer',
        verbose_name='Виробник',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='products'
    )
    category = models.ForeignKey(
        'Subcategory',
        verbose_name='Категорія',
        on_delete=models.PROTECT,
        related_name='products'
    )
    selling = models.BooleanField(verbose_name='Продаж', default=True)
    average_rating = models.FloatField(verbose_name='Рейтинг', default=0)
    photo = models.ImageField(verbose_name='Фото', upload_to='photos_product/%Y/%m/%d/')
    description = models.TextField(verbose_name='Опис товару')
    evaluated_cnt = models.PositiveBigIntegerField(verbose_name='Оцінено раз', default=0)
    added = models.DateField(verbose_name='Додано', auto_now_add=True)
    discount = models.PositiveSmallIntegerField(verbose_name='Знижка', default=0)
    slug = AutoSlugField(populate_from='name', max_length=150, unique=True, db_index=True, verbose_name="URL")

    def get_actual_price(self):
        return self.price - (self.price * self.discount/100)

    def get_absolute_url(self):
        return reverse_lazy('shop:product-detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'
        ordering = ['-added']


class ProductParameter(models.Model):
    name = models.CharField(max_length=50, verbose_name='Назва типу параметру')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Параметр товару'
        verbose_name_plural = 'Параметри товарів'


class ProductOptions(models.Model):
    name = models.CharField(max_length=50, verbose_name='Варіант товару')
    parameter = models.ForeignKey(
        'ProductParameter',
        verbose_name='Тип варіанту',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        'Product',
        verbose_name='Продукт',
        on_delete=models.CASCADE,
        related_name='options'
    )
    surcharge = models.FloatField(verbose_name='Доплата', null=True, default=0, help_text='необов\'язково')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Опція до товару'
        verbose_name_plural = 'Опції до товарів'


class PhotoProduct(models.Model):
    photo = models.ImageField(upload_to='photos_product/%Y/%m/%d/')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='photos')


class Review(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='reviews')
    user_name = models.CharField(verbose_name='Ім\'я', max_length=60)
    text = models.TextField(verbose_name='Відгук')
    rating = models.PositiveSmallIntegerField(verbose_name='Рейтинг продукту', validators=[validators.MinValueValidator(1),
                                                                                           validators.MaxValueValidator(5)])
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Відгук до товару - {self.product}'

    class Meta:
        verbose_name = 'Відгук'
        verbose_name_plural = 'Відгуки'


class Manufacturer(models.Model):
    name = models.CharField(verbose_name='Бренд', max_length=70)
    category = models.ForeignKey(
        'Category',
        verbose_name='Категорія товарів, які виготовляє виробник',
        on_delete=models.PROTECT,
        related_name='manufacturers'
    )
    slug = AutoSlugField(populate_from='name', max_length=80, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Виробник'
        verbose_name_plural = 'Виробники'


class Category(models.Model):
    name = models.CharField(verbose_name='Категорія', max_length=70)
    slug = AutoSlugField(populate_from='name', max_length=150, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'


class Subcategory(models.Model):
    name = models.CharField(verbose_name='Підкатегорія', max_length=70)
    parent_category = models.ForeignKey(
        'Category',
        verbose_name='Батьківська категорія',
        on_delete=models.PROTECT,
        related_name='subcategories'
    )
    slug = AutoSlugField(populate_from='name', max_length=150, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Підкатегорія'
        verbose_name_plural = 'Підкатегорії'


class Banner(models.Model):
    name = models.CharField(verbose_name='Назва', max_length=50,
                            help_text='Потрібно для того, щоб було зручніше працювати із обєктами банерів')
    image = models.ImageField(verbose_name='Банер', upload_to='banners/%m/')
    url = models.URLField(blank=True, help_text='Посилання, яке веде на категорію, товар і тд.')
    draft = models.BooleanField(verbose_name='Чернетка', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Банер'
        verbose_name_plural = 'Банери'



