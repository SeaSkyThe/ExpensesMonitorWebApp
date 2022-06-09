from pydoc import describe
from unicodedata import category
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreferences
# Create your views here.


def search_expenses(request):
	if(request.method == 'POST'):
		search_string = json.loads(request.body).get('searchText')
		expenses = Expense.objects.filter(price__startswith=search_string, owner=request.user) | Expense.objects.filter(
			date__startswith=search_string, owner=request.user)	| Expense.objects.filter(
			description__icontains=search_string, owner=request.user) | Expense.objects.filter(
			category__icontains=search_string, owner=request.user) 

		data = expenses.values()

		return JsonResponse(list(data), safe=False)
		
@login_required(login_url='/authentication/login')
def index(request):
	categories=Category.objects.all()
	if(request.method == 'GET'):
		expenses = Expense.objects.filter(owner=request.user).values().order_by('-date')
		paginator = Paginator(expenses, per_page=7)
		page_number = request.GET.get('page')
		page_object = paginator.get_page(page_number)
		
		if(UserPreferences.objects.filter(user=request.user).exists()):
			currency = UserPreferences.objects.get(user=request.user).currency
		else:
			currency = 'Brazilian Real - BRL'
			userpreferences = UserPreferences(user=request.user, currency=currency)
			userpreferences.save()
		
		context = {
			'expenses' : expenses,
			'page_object' : page_object,
			'currency' : currency, 
		}
		return render(request, 'expenses/index.html', context)
		

	return render(request, 'expenses/index.html')
	
@login_required(login_url='/authentication/login')
def add_expense(request):
	categories=Category.objects.all()
	context = {
		'categories': categories,
		'values': request.POST
	}
	


	if(request.method == 'POST'):
		price = request.POST['price']
		description = request.POST['description']
		spending_date = request.POST['spending_date']
		category = request.POST['category']

		if(not price):
			messages.error(request, 'Price is a required field')
			return render(request, 'expenses/add_expense.html', context)

		if(not description):
			messages.error(request, 'Description is a required field')
			return render(request, 'expenses/add_expense.html', context)

		if(not spending_date):
			messages.error(request, 'Date is a required field')
			return render(request, 'expenses/add_expense.html', context)
		
		Expense.objects.create(price=price, description=description, category=category, date=spending_date, owner=request.user)
		messages.success(request, 'Expense saved succesfully')

		return redirect('expenses')

	return render(request, 'expenses/add_expense.html', context)



def edit_expense(request, id):
	categories=Category.objects.all()
	expense = Expense.objects.get(pk=id)
	context = {
		'values': expense,
		'categories': categories,
	}
	
	if(request.method == 'GET'):
		messages.info(request, 'Edit your expense')
		return render(request, 'expenses/edit_expense.html', context)

	if(request.method == 'POST'):

		price = request.POST['price']
		description = request.POST['description']
		spending_date = request.POST['spending_date']
		category = request.POST['category']

		if(not price):
			messages.error(request, 'Price is a required field')
			return render(request, 'expenses/edit_expense.html', context)

		if(not description):
			messages.error(request, 'Description is a required field')
			return render(request, 'expenses/edit_expense.html', context)

		if(not spending_date):
			messages.error(request, 'Date is a required field')
			return render(request, 'expenses/edit_expense.html', context)
		
		
		expense.price = price
		expense.description = description
		expense.category = category
		expense.date = spending_date
		expense.owner = request.user
		expense.save()

		messages.success(request, 'Expense updated succesfully')

		return redirect('expenses')

def delete_expense(request, id):
	expense = Expense.objects.get(pk=id)
	expense.delete()
	messages.success(request, 'Expense deleted succesfully')
	return redirect('expenses')