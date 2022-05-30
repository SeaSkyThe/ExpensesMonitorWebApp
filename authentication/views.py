from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
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
	def get(self, request): #When receives a get request - Client requests a page
		return render(request, 'authentication/register.html')


	def post(self, request): #When receives a post request - Client sends something to this address


		#Getting user data
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
			#Context variable to keep the form fields after an error
		context = {
			'fieldValues': request.POST,
		}

		#Validate - besides the form input validation that we have done in register.js file.
		if(not User.objects.filter(username=username).exists()): # Make sure that the username was not used before
			if(not User.objects.filter(email=email).exists()): # Make sure that the email was not used
				if(len(password) < 6): # Password has to be greater than 6
					messages.error(request, 'Your password is too short.')
					return render(request, 'authentication/register.html', context=context)

				#Create account
				user = User.objects.create_user(username=username, email=email)
				user.set_password(password)
				user.save()

				messages.success(request, 'The registration was a sucess!')
				return render(request, 'authentication/register.html')


		return render(request, 'authentication/register.html')