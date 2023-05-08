from django import forms


class ContactForm(forms.Form):
    first_name = forms.CharField(
        label='First name',
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'size': 40,
                'class': 'required',
                'title': 'Name must be between 3 and 32 characters!'
            }
        )
    )
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(
            attrs={
                'type': 'text',
                'size': 40,
                'class': 'required email',
                'title': 'E-Mail Address does not appear to be valid!'
            }
        )
    )
    text = forms.CharField(
        label='Message',
        widget=forms.Textarea(
            attrs={
                'id': 'enquiry',
                'style': 'width: 98%;',
                'rows': 10,
                'class': 'required',
                'title': 'Enquiry must be between 10 and 3000 characters!'
            }
        )
    )
