from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
# Create your views here.

# Validate the entered email
class EmailValidationView(View):
	def post(self, request):
		# Load the request body as a json and gets the email (basically, getting the 'email' field from the form)
		data = json.loads(request.body)
		email = data['email']

		# Verify if the email is valid
		if(not validate_email(email)):
			return JsonResponse({'email_error':  "Emails should be in the format: 'example@domain.com'. Try another one."})
		# Verify if the email is already taken
		if(User.objects.filter(email=email).exists()):
			return JsonResponse({'email_error': 'This email was already taken, choose another one.'}, status=409)

		return JsonResponse({'email_valid': True})

# Validate the entered username
class UsernameValidationView(View):
	def post(self, request):
		# Load the request body as a json and gets the username (basically, getting the 'username' field from the form)
		data = json.loads(request.body)
		username = data['username']

		# Verify if the username is alphanumeric and returning error if not
		if(not str(username).isalnum()):
			return JsonResponse({'username_error': 'Username should only contain alphanumeric characters. (A-Z, a-z, 0-9)'}, status=400)
		
		# Verify if the username is already taken
		if(User.objects.filter(username=username).exists()):
			return JsonResponse({'username_error': 'This username was already taken, choose another one.'}, status=409)

		return JsonResponse({'username_valid': True})

class RegistrationView(View):
	def get(self, request):
		return render(request, 'authentication/register.html')