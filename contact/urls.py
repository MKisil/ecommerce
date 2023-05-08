from django.urls import path

from contact.views import AboutShoppicaView, ContactShoppicaView

urlpatterns = [
    path('', ContactShoppicaView.as_view(), name='contact'),
    path('about/', AboutShoppicaView.as_view(), name='about')
]
