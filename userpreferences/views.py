from django.shortcuts import render
import os 
import json
from django.conf import settings
from django.contrib import messages

from .models import UserPreferences


# Create your views here.

def index(request):
    user_preferences = None
    userPreferences_exists = UserPreferences.objects.filter(user = request.user).exists()
    
    if(userPreferences_exists): # If the user preference exists, we get and change, if not, we create
        user_preferences = UserPreferences.objects.get(user = request.user)
    else:
        user_preferences = UserPreferences(user=request.user, currency='Brazilian Real - BRL')
        user_preferences.save()

    currencies_data = []
    currencies_path = os.path.join(settings.BASE_DIR, 'Common-Currency.json')


    with open(currencies_path, 'r', encoding='utf-8') as json_file:
        
        data = json.load(json_file)

        for key, value in data.items():
            currencies_data.append({'name': value['name'], 'code': key, 'symbol': value['symbol']})
    
    #POST
    if request.method == 'POST':
        
        currency = request.POST['currency']
        
        if(userPreferences_exists):
            if(user_preferences.currency != currency):
                user_preferences.currency=currency
                user_preferences.save()
        else:
            UserPreferences.objects.create(user=request.user, currency=currency)

        messages.success(request, 'Changes saved')

    return render(request, 'userpreferences/index.html', {'currencies': currencies_data, 'user_preferences': user_preferences})

    

