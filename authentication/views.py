from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.core.mail import EmailMessage
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
			return JsonResponse({'email_error': 'This email was already taken, choose another one.', 'status_code': 409}, status=409)

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
				# #Set active to false, and to be active, the user has to confirm his/her email.
				# user.is_active = False
				
				#Saves the user in Database
				user.save()

				# #Send confirmation mail to the user
				# subject = 'Expenses App Account Confirmation Email'
				# body = ''
				# from_email = 'noreply@sst.com'

				# email_message = EmailMessage(
				#     subject=subject,
				#     body=body,
				#     from_email=from_email,
				#     [email]
				# )

				messages.success(request, 'The registration was a sucess!')
				return render(request, 'authentication/register.html')


		return render(request, 'authentication/register.html')


class LoginView(View):
	def get(self, request):
		return render(request, 'authentication/login.html')

	def post(self, request):
		username = request.POST['username']
		password = request.POST['password']

		if(username and password):
			user = auth.authenticate(username=username, password=password)

			if(user):
				if(user.is_active):
					auth.login(request, user)
					messages.success(request, f'Welcome, {user.username} you are now logged in')
					return redirect('expenses')

				messages.error(request, f'This account is not active, please check your email or talk with an admin.')
				return render(request, 'authentication/login.html')

			messages.error(request, f'Invalid credentials, please try again')
			return render(request, 'authentication/login.html')
		
		messages.error(request, f'Please fill all fields')
		return render(request, 'authentication/login.html')


class LogoutView(View):
	def post(self, request):
		auth.logout(request)
		messages.success(request, 'You have been logged out')
		return redirect('login')

class ResetPasswordView(View):
	


	def get(self, request):
		return render(request, 'authentication/reset_password.html')

	def post(self, request):
		context = {
			'fieldValues': request.POST,
		}

		email = request.POST['email']
		username = request.POST['username']
		password = request.POST['newPassword']
		password_repeat = request.POST['newPasswordRepeat']

		if(password != password_repeat):
			messages.error(request, 'Passwords does not match, try again')
			return render(request, 'authentication/reset_password.html', context)

		if(len(password) < 6):
			messages.error(request, 'Passwords must have 6 characters or more.')
			return render(request, 'authentication/reset_password.html', context)

		if(not User.objects.filter(username=username).exists()): # If username does not exists or its empty
			if(username == ''):
				messages.error(request, 'Username is a required field')
			else:
				messages.error(request, 'This username does not exists in our database, try again')
			return render(request, 'authentication/reset_password.html', context)

		if(not User.objects.filter(email=email, username=username).exists()):# If email does not match with that username or is empty
			if(email==''):
				messages.error(request, 'Email is a required field')
			else:
				messages.error(request, 'This email does not exists in our database, or it does not belong to that username, try again')
			return render(request, 'authentication/reset_password.html', context)
		
		
		# everything ok
		user = User.objects.get(username=username, email=email)
		user.username = username
		user.email = email
		user.set_password(password)
		user.save()
		messages.success(request, 'Password reseted successfully')
		
		return redirect('login')