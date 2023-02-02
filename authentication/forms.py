from django import forms
from django.contrib.auth.forms import UserCreationForm

from authentication.models import MyUser


class RegistrationForm(forms.ModelForm):

    username = forms.CharField(
        label='Enter Username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required': 'Sorry, you will need an email'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('username', 'email',)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = MyUser.objects.filter(username=username)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if MyUser.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email
