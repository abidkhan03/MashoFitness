from django.urls import path
from . import views
from employees.views import index

urlpatterns = [
    path('index/', index, name='index'),
    path("supplier/", views.supplier, name="supplier"),
    path("updateSupplier/", views.updateSupplier, name="updateSupplier"),
    

    # api path
    path('api/SearchBySupplierField/', views.SearchBySupplierField, name='SearchBySupplierField'),
    path('api/deleteSupplier/', views.deleteSupplier, name='deleteSupplier'),
    path('api/getSupplierDetails/', views.getSupplierDetails, name='getSupplierDetails'),
]