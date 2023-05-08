from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django_registration.forms import RegistrationForm

from shop.models import Review


User = get_user_model()


class CustomRegistrationForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User


class ReviewForm(forms.ModelForm):
    CHOICES_RATING = ((1, 'Bad'),
                      (2, 'Poor'),
                      (3, 'Average'),
                      (4, 'Good'),
                      (5, 'Excellent'))

    user_name = forms.CharField(label='Your Name')
    text = forms.CharField(label='Your Review', widget=forms.Textarea(attrs={'style': 'width: 98%', 'row': 8}))
    rating = forms.ChoiceField(label='Rating', widget=forms.RadioSelect(attrs={'inline': True}), choices=CHOICES_RATING)

    class Meta:
        model = Review
        fields = ('user_name', 'text', 'rating')


class EmailForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100, required=True, help_text='Введіть ваш email адрес')

    def clean(self):
        cleaned_data = super().clean()

        if self.errors:
            return cleaned_data

        user_email = cleaned_data['email']
        try:
            user = User.objects.get(email=user_email)
        except ObjectDoesNotExist:
            raise forms.ValidationError('Введіть корректну email адресу')

        cleaned_data['user'] = user
        return cleaned_data






