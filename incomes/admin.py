from django.contrib import admin
from .models import Income, Source
# Register your models here.


class IncomeAdmin(admin.ModelAdmin):
    list_display = ('amount', 'description', 'source', 'date')
    search_field = ('description', 'source', 'date')

admin.site.register(Income, IncomeAdmin)

admin.site.register(Source)
