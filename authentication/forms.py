from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, UserCreationForm

from authentication.models import MyUser


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        label='Enter Username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required': 'Sorry, you will need an email'})

    class Meta:
        model = MyUser
        fields = ('username', 'email', 'password1', 'password2', )

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = MyUser.objects.filter(username=username)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if MyUser.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email


class PsswrdResetForm(PasswordResetForm):

    email = forms.EmailField(max_length=254,
                             widget=forms.TextInput(
                                 attrs={'placeholder': 'email'}
                             ))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = MyUser.objects.filter(email=email)
        if not user:
            raise forms.ValidationError(
                'No such email in the database'
            )
        return email


class PsswrdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))

