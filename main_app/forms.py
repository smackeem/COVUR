from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Customer, Review


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

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['stars', 'content']
    
    STARS_CHOICES = [
        (5, '5 stars'),
        (4, '4 stars'),
        (3, '3 stars'),
        (2, '2 stars'),
        (1, '1 star'),
    ]

    stars = forms.ChoiceField(
        choices=STARS_CHOICES,
        # widget=forms.Select(attrs={'class': 'form-control'})
    )
