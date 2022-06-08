from django.contrib import admin
from .models import Expense, Category
# Register your models here.

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('price', 'description', 'category', 'date')
    search_field = ('description', 'category', 'date')

admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Category)
