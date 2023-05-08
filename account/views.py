from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy

from account.forms import LoginUserForm


class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = 'registration/account.html'

    def get_success_url(self):
        return reverse_lazy('shop:home')


def logout_user(request):
    cart = request.session['cart']
    logout(request)
    request.session['cart'] = cart
    return redirect('shop:home')


def register_or_guest(request):
    if request.GET['action'] == 'register':
        return redirect('django_registration_register')
    else:
        return redirect('checkout')
