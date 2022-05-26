from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
# Create your views here.

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
			return JsonResponse({'username_error': 'This is username was already taken, choose another one.'}, status=409)

		return JsonResponse({'username_valid': True})

class RegistrationView(View):
	def get(self, request):
		return render(request, 'authentication/register.html')