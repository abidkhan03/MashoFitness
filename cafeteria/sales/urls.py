from django.urls import  path
from . import views
from employees.views import index

urlpatterns = [
    path('index/', index, name='index'),
    path("sales/", views.sales, name="sales"),
    path("salesReturn/", views.salesReturn, name="salesReturn"),

    # api sales
    path("api/cafeteria/sales/get_sale/<int:pk>", views.GetsalesApi, name="salesApi"),
    path("api/cafeteria/sales/search_sales_invoiceID/<int:pk>", views.GetsalesInvoiceIDsearchApi, name="invoiceIDsearchApi"),
    path("api/cafeteria/sales/search_sales_customer/", views.GetsalesCustomerSearchApi, name="customerIDsearchApi"),

    # api salesReturn
    path("api/cafeteria/salesReturn/get_sale/<int:pk>", views.GetsalesReturnApi, name="salesReturnApi"),
    path("api/cafeteria/salesReturn/search_sales_invoiceID/<int:pk>", views.GetsalesReturnInvoiceIDsearchApi, name="salesReturninvoiceIDsearchApi"),
    path("api/cafeteria/salesReturn/search_sales_customer/", views.GetsalesReturnCustomerSearchApi, name="salesReturncustomerIDsearchApi"),
]