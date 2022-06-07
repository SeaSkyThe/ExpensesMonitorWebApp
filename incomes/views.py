from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Source, Income
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreferences

# Create your views here.
@login_required(login_url='/authentication/login')
def index(request):
	sources=Source.objects.all()
	if(request.method == 'GET'):
		incomes = Income.objects.filter(owner=request.user).values().order_by('-date')
		paginator = Paginator(incomes, per_page=5)
		page_number = request.GET.get('page')
		page_object = paginator.get_page(page_number)

		currency = UserPreferences.objects.get(user=request.user).currency
		context = {
			'incomes' : incomes,
			'page_object' : page_object,
			'currency' : currency, 
		}
		return render(request, 'incomes/index.html', context)
		

	return render(request, 'incomes/index.html')
	
@login_required(login_url='/authentication/login')
def add_income(request):
    sources=Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }
	
    if(request.method == 'POST'):
        print(request.POST.keys())
        amount = request.POST['amount']
        description = request.POST['description']
        income_date = request.POST['income_date']
        source = request.POST['source']
        

        if(not source):
            messages.error(request, 'Source is a required field')
            return render(request, 'incomes/add_income.html', context)

        if(not amount):
            messages.error(request, 'Amount is a required field')
            return render(request, 'incomes/add_income.html', context)

        if(not description):
            messages.error(request, 'Description is a required field')
            return render(request, 'incomes/add_income.html', context)

        if(not income_date):
            messages.error(request, 'Date is a required field')
            return render(request, 'incomes/add_income.html', context)

        
        Income.objects.create(amount=amount, description=description, source=source, date=income_date, owner=request.user)
        messages.success(request, 'Income saved succesfully')

        return redirect('incomes')

    return render(request, 'incomes/add_income.html', context)


def edit_income(request, id):
	sources=Source.objects.all()
	income = Income.objects.get(pk=id)
	context = {
		'values': income,
		'sources': sources,
	}
	
	if(request.method == 'GET'):
		messages.info(request, 'Edit your income')
		return render(request, 'incomes/edit_income.html', context)

	if(request.method == 'POST'):

		amount = request.POST['amount']
		description = request.POST['description']
		income_date = request.POST['income_date']
		source = request.POST['source']

		if(not amount):
			messages.error(request, 'Amount is a required field')
			return render(request, 'incomes/edit_income.html', context)

		if(not description):
			messages.error(request, 'Description is a required field')
			return render(request, 'incomes/edit_income.html', context)

		if(not income_date):
			messages.error(request, 'Date is a required field')
			return render(request, 'incomes/edit_income.html', context)
		
		
		income.amount = amount
		income.description = description
		income.source = source
		income.date = income_date
		income.owner = request.user
		income.save()

		messages.success(request, 'Income updated succesfully')

		return redirect('incomes')

def delete_income(request, id):
	income = Income.objects.get(pk=id)
	income.delete()
	messages.success(request, 'Income deleted succesfully')
	return redirect('incomes')