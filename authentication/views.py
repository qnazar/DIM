from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import RegistrationForm
from .models import MyUser
from .token import account_activation_token


@login_required
def dashboard(request):
    return render(request,
                  'authentication/dashboard.html',
                  {'section': 'profile'})


def registration(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # EMAIL SETUP
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('authentication/account_activation_email.html',
                                       {'user': user, 'domain': current_site,
                                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                        'token': account_activation_token.make_token(user),
                                        })
            user.email_user(subject=subject, message=message)
            # END EMAIL PART

            return render(request, 'authentication/registration_success.html')  #  HttpResponseRedirect('/')
    else:
        form = RegistrationForm()
        return render(request, 'authentication/registration.html', {'form': form})


def confirm_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('auth:dashboard')
    else:
        return HttpResponse('Activation invalid')
