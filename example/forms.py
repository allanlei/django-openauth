from django import forms

class LoginForm(forms.Form):
    domain = forms.CharField()
