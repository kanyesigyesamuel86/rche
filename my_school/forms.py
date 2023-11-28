from django import forms
from .models import NewUser
from django.contrib import messages

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = NewUser
        fields = ['username','first_name', 'last_name', 'password', 'confirm_password', 'email', 'class_name']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match. Please confirm your password.")
 


class LoginForm(forms.Form):
    username = forms.CharField(
    max_length=150,
    widget=forms.TextInput(attrs={'class': 'custom-input'})
    )
    password = forms.CharField(
    widget=forms.PasswordInput(attrs={'class': 'custom-input'}),
    help_text='Must have at least one lowercase, one uppercase, a digit, and a special character'
)


