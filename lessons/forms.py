from django import forms

#These are just placeholder forms
class LogInForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

class SignUpForm(forms.Form):
    print("test")

class NewBookingForm(forms.Form):
    test = forms.CharField(label="TEST")
