from django.urls import path
from . import views
from employees.views import index

urlpatterns = [
    path('index/', index, name='index'),
    path("cafeteriaExpenses/", views.cafeteriaExpenses, name="cafeteriaExpenses"),
    path("updateCafeteriaExpenses/", views.updateCafeteriaExpenses, name="updateCafeteriaExpenses"),

    # api path
    path("api/deleteCafeteriaExpense/", views.deleteCafeteriaExpense, name="deleteCafeteriaExpense"),
    # path("api/searchByExpenseDate/", views.searchByExpenseDate, name="searchByExpenseDate"),
    path("api/searchByCafeteriaExpenseHeadOfAccount/", views.searchByCafeteriaExpenseHeadOfAccount, name="searchByCafeteriaExpenseHeadOfAccount"),
    path("api/searchByCafeteriaExpenseDate/", views.searchByCafeteriaExpenseDate, name="searchByCafeteriaExpenseDate"),
    # path("api/searchByModule/", views.searchByModule, name="searchByModule"),
]