from django.urls import path, reverse
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from .views import registration, confirm_email, dashboard, edit_details, delete_user
from .forms import PsswrdResetForm, PsswrdResetConfirmForm

urlpatterns = [
    path('registration/', registration, name='registration'),
    path('registration/confirm_email/<slug:uidb64>/<slug:token>', confirm_email, name='confirm_email'),
    path('login/', auth_views.LoginView.as_view(template_name='authentication/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('dashboard/', dashboard, name='dashboard'),  # TODO move to other place
    path('dashboard/edit/', edit_details, name='edit_details'),
    path('dashboard/delete/', delete_user, name='delete_user'),
    path('dashboard/delete/confirm', TemplateView.as_view(
        template_name='authentication/delete_confirm.html'
    ), name='delete_confirm'),

    # path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    # path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='authentication/password_reset_form.html',
        success_url='/auth/password_reset/confirm/',
        email_template_name='authentication/password_reset_email.html',
        form_class=PsswrdResetForm
    ), name='password_reset'),

    path('password_reset/confirm/', TemplateView.as_view(
        template_name="authentication/reset_status.html"
    ), name='password_reset_done'),

    path('password_reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='authentication/password_reset_confirm.html',
        success_url='/auth/password_reset/complete/',
        form_class=PsswrdResetConfirmForm
    ), name='password_reset_confirm'),

    path('password_reset/complete/', TemplateView.as_view(
        template_name="authentication/reset_status.html"
    ), name='password_reset_complete'),
]
