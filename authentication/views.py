from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import RegistrationForm


def registration(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = RegistrationForm()
        return render(request, 'authentication/registration.html', {'form': form})
