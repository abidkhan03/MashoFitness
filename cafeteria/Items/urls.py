from django.urls import path
from . import views
from employees.views import index

urlpatterns = [
    path('index/', index, name='index'),
    path("addItem/", views.addItem, name="addItem"),
    path("addNonStockItem/", views.addNonStockItem, name="addNonStockItem"),
    path("pos/", views.pos, name="pos"),
    path("barcodeLabel/", views.barcodeLabel, name="barcodeLabel"),
    

    # api path
    path("api/SearchByItemField/", views.SearchByItemField, name='SearchByItemField'),
    path("api/SearchByStockField/", views.SearchByStockField, name='SearchByStockField'),
    path("api/UpdateItemQueryCall/", views.UpdateItemQueryCall, name='UpdateItemQueryCall'),
    path("api/UpdateNonStockQueryCall/", views.UpdateNonStockQueryCall, name='UpdateNonStockQueryCall'),
    path("api/ItemCodeCheck/", views.ItemCodeCheck, name='ItemCodeCheck'),
    path("api/ItemNameCheck/", views.ItemNameCheck, name='ItemNameCheck'),
    path("api/NonStockItemCodeCheck/", views.NonStockItemCodeCheck, name='NonStockItemCodeCheck'),
    path("api/NonStockItemNameCheck/", views.NonStockItemNameCheck, name='NonStockItemNameCheck'),
]