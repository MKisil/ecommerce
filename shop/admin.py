from django.contrib import admin
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from .models import *


class ProductForm(forms.ModelForm):
    add_to_quantity = forms.IntegerField(label='Додати кількість товару', required=False)

    def clean(self):
        cleaned_data = super().clean()
        add_to_quantity = cleaned_data.get('add_to_quantity')

        if add_to_quantity is not None and self.instance.quantity + add_to_quantity < 0:
            raise forms.ValidationError('Число товарів на складі не може бути від\'ємним')
        return cleaned_data

    class Meta:
        model = Product
        fields = '__all__'


class OptionInline(admin.TabularInline):
    model = ProductOptions
    extra = 1


class PhotoInline(admin.StackedInline):
    model = PhotoProduct
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm

    list_display = ('id', 'name', 'selling',)
    list_display_links = ('id', 'name')
    list_filter = ('category',)
    autocomplete_fields = ['manufacturer']
    search_fields = ('id', 'name')
    inlines = [OptionInline, PhotoInline]
    save_on_top = True
    save_as = True
    list_editable = ('selling',)
    readonly_fields = ('get_rating', 'evaluated_cnt', 'get_photo')

    fields = ('name', 'price', 'discount', 'model',
              'manufacturer', 'category', 'quantity', 'selling', 'get_rating',
              'evaluated_cnt', 'photo', 'get_photo', 'description',
              'add_to_quantity',
              )

    def get_rating(self, obj):
        if obj.average_rating:
            return obj.average_rating
        else:
            return 'ще ніхто не оцінював цей товар'

    def get_photo(self, obj):
        return mark_safe(f"<img src={obj.photo.url} width='50' height='auto'>")

    get_rating.short_description = 'Рейтинг'
    get_photo.short_description = 'Поточна фотографія товару'

    def save_model(self, request, obj, form, change):
        add_to_quantity = form.cleaned_data['add_to_quantity']
        if add_to_quantity:
            obj.quantity += add_to_quantity
        return super().save_model(request, obj, form, change)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass


admin.site.register(ProductParameter)
admin.site.register(Banner)


