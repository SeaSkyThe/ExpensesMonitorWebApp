from pydoc import describe
from unicodedata import category
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
# Create your views here.

@login_required(login_url='/authentication/login')
def index(request):
	categories=Category.objects.all()
	if(request.method == 'GET'):
		expenses = Expense.objects.filter(owner=request.user).values().order_by('-date')
		context = {
			'expenses' : expenses
		}
		return render(request, 'expenses/index.html', context)
		pass

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