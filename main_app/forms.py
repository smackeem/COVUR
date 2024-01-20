from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Customer


class SignUpForm(UserCreationForm):
    first_name = forms.CharField( max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField( max_length=254, required=True)

    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
  
    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        exist = Customer.objects.filter(email=email).exits()  
        if exist:  
            raise ValidationError(" Email Already Exist")  
        return email

    
