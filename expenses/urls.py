from django.urls import path

from . import views

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='expenses'),
    path('add_expense', views.add_expense, name="add_expense"),
    path('edit_expense/<int:id>', views.edit_expense, name="edit_expense"),
    path('delete_expense/<int:id>', views.delete_expense, name="delete_expense"),
    path('search_expenses/', csrf_exempt(views.search_expenses), name="search_expenses"),
    path('expenses_category_summary/', views.expenses_category_summary, name="expenses_category_summary"),
    path('expenses_stats_view/', views.expenses_stats_view, name="expenses_stats"),
]
