from django.contrib import admin

from contact.models import Contact, ShopAddress

admin.site.register(ShopAddress)
admin.site.register(Contact)