from django.core.mail import send_mail
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from contact.forms import ContactForm
from contact.models import ShopAddress, Contact
from internet_shop import settings


class AboutShoppicaView(TemplateView):
    template_name = 'contact/about.html'


class ContactShoppicaView(FormView):
    template_name = 'contact/contact.html'
    form_class = ContactForm

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = 'New message from your store'
            message = f'Name: {form.cleaned_data["first_name"]}\nEmail: {form.cleaned_data["email"]}\nMessage: {form.cleaned_data["text"]}'
            send_mail(
                subject,
                message,
                form.cleaned_data["email"],
                [settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            return redirect('shop:home')
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['addresses'] = ShopAddress.objects.all()
        context['contacts'] = Contact.objects.all()
        return context
