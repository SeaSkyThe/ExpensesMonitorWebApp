from .views import RegistrationView, UsernameValidationView, EmailValidationView, LoginView, LogoutView, ResetPasswordView
from django.urls import path

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
	path('register', RegistrationView.as_view(), name='register'), #as_view() because its a class
	path('login', LoginView.as_view(), name='login'), #as_view() because its a class
	path('logout', csrf_exempt(LogoutView.as_view()), name='logout'), #as_view() because its a class
	path('validate_username', csrf_exempt(UsernameValidationView.as_view()), name='validate_username'),
	path('validate_email', csrf_exempt(EmailValidationView.as_view()), name='validate_email'),
	path('reset_password', csrf_exempt(ResetPasswordView.as_view()), name='reset_password'),
]