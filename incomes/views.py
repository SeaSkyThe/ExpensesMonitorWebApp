from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Source, Income
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreferences
import datetime

# Create your views here.
@login_required(login_url='/authentication/login')
def index(request):
	sources=Source.objects.all()
	if(request.method == 'GET'):
		incomes = Income.objects.filter(owner=request.user).values().order_by('-date')
		paginator = Paginator(incomes, per_page=7)
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

def search_incomes(request):
	if(request.method == 'POST'):
		search_string = json.loads(request.body).get('searchText')
		incomes = Income.objects.filter(amount__startswith=search_string, owner=request.user) | Income.objects.filter(
			date__startswith=search_string, owner=request.user)	| Income.objects.filter(
			description__icontains=search_string, owner=request.user) | Income.objects.filter(
			source__icontains=search_string, owner=request.user) 

		data = incomes.values()

		return JsonResponse(list(data), safe=False)



# Graphs Views

def incomes_source_summary(request):
	today_date = datetime.date.today()
	six_months_ago = today_date-datetime.timedelta(days=30*6)

	user_incomes_last_six_months = Income.objects.filter(date__gte=six_months_ago, date__lte=today_date,owner=request.user)

	data_for_graph = {}

	def get_source_from_income(income):
		return income.source

	source_list = list(set(map(get_source_from_income, user_incomes_last_six_months)))

	def get_income_source_amount(source):
		total_amount = 0
		filtered_by_source = user_incomes_last_six_months.filter(source=source)

		for item in filtered_by_source:
			total_amount = total_amount + item.amount

		return total_amount

	
	for source in source_list:
		data_for_graph[source] = get_income_source_amount(source)

	return JsonResponse({'income_source_data': data_for_graph}, safe=False)


def incomes_stats_view(request):
	return render(request, 'incomes/stats.html')