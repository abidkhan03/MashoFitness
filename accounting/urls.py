from django.urls import path
from . import views
from employees.views import index

urlpatterns = [
    path('index/', index, name='index'),
    path('expensesReport/', views.expensesReport, name='expensesReport'),
    path('reports/', views.reports, name='reports'),
    path('revenue/', views.revenue, name="revenue"),
]

