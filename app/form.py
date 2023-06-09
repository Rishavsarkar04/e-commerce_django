from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm ,UsernameField , PasswordChangeForm , PasswordResetForm , SetPasswordForm
from django.contrib.auth import password_validation
from .models import Customer

class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField( required=True , widget=forms.EmailInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email','password1','password2']
        labels = {'email':'Email Address'}
        widgets = {'username': forms.TextInput(attrs={'class':'form-control'})}

class LoginForm(AuthenticationForm):
    username = UsernameField(widget = forms.TextInput(attrs={'autofocus': True , 'class':'form-control'}))
    password = forms.CharField(widget = forms.PasswordInput(attrs={'autocomplete': 'current-password' , 'class':'form-control'}))
    
class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="old password",widget=forms.PasswordInput( attrs={"autocomplete": "current-password", "autofocus": True}))
    new_password1 = forms.CharField(label="new password",widget=forms.PasswordInput( attrs={"autocomplete": "new-password", "autofocus": True}),help_text= password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label="confirm new password",widget=forms.PasswordInput( attrs={"autocomplete": "new-password", "autofocus": True}))

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Email Address', widget=forms.EmailInput(attrs={"autocomplete": "email",'class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label="new password",widget=forms.PasswordInput( attrs={"autocomplete": "new-password", "autofocus": True}),help_text= password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label="confirm new password",widget=forms.PasswordInput( attrs={"autocomplete": "new-password", "autofocus": True}),help_text= password_validation.password_validators_help_text_html())

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model= Customer
        exclude =  ('user',)
        widgets = {'name': forms.TextInput(attrs={'class':'form-control'}),
                    'locality': forms.TextInput(attrs={'class':'form-control'}),
                    'city': forms.TextInput(attrs={'class':'form-control'}),
                    'state': forms.Select(attrs={'class':'form-control'}),
                    'zipcode': forms.NumberInput(attrs={'class':'form-control'}),}