from django.urls import path, include

from account.views import LoginUserView, register_or_guest, logout_user

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('action/', register_or_guest, name='action'),
    path('', include('django.contrib.auth.urls')),
]
