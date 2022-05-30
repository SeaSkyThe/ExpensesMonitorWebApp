from .views import RegistrationView, UsernameValidationView, EmailValidationView
from django.urls import path

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
	path('register', RegistrationView.as_view(), name='register'), #as_view() because its a class
	path('validate_username', csrf_exempt(UsernameValidationView.as_view()), name='validate_username'),
	path('validate_email', csrf_exempt(EmailValidationView.as_view()), name='validate_email'),
]