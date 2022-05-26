from .views import RegistrationView
from django.urls import path

urlpatterns = [
	path('register', RegistrationView.as_view()), #as_view() because its a class

]